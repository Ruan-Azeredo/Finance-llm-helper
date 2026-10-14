# Guia de Arquitetura de Deploy: GitHub Actions + GHCR + Coolify (Hetzner)

Este guia documenta o padrão arquitetural para deploy contínuo em servidores de baixo custo (ex.: Hetzner CX22/CAX11, DigitalOcean $4-$6, Linode) gerenciados pelo **Coolify**, eliminando travamentos de CPU, esgotamento de memória e quedas de serviço durante o deploy.

---

## 1. O Problema

Em servidores pequenos com 1 a 2 vCPUs e 2 a 4 GB de RAM:
- O Coolify, por padrão, executa o `docker build` **diretamente dentro da VPS** ao receber o webhook do Git.
- Durante a instalação e compilação de dependências pesadas (`pip install`, `npm build`, compilação C/Rust, etc.), o Docker BuildKit consome **100% de todos os núcleos da CPU** e atinge o teto da memória RAM.
- Como essas VPSs frequentemente vêm com **0 MB de SWAP**, o kernel Linux entra em *lockup/thrashing* ou o *OOM Killer* mata processos críticos.
- **Consequência:** O Coolify para de responder, o SSH trava, o deploy fica travado e o servidor precisa de hard reset no painel da nuvem.

---

## 2. A Solução Arquitetural

**Desacoplar o ambiente de compilação (Build) do ambiente de execução (Runtime):**

1. O **GitHub Actions** (máquinas gratuitas com 16GB de RAM e 4 vCPUs) compila o Dockerfile e gera a imagem.
2. A imagem é enviada para o **GitHub Container Registry (`ghcr.io`)**.
3. O GitHub Actions dispara o Webhook do Coolify.
4. O **Coolify na Hetzner** executa apenas um leve `docker pull` da imagem já compilada e sobe o container.

> 📊 **Diagrama visual interativo:** Abra o arquivo [ci_cd_strategy_flow.html](./ci_cd_strategy_flow.html) no seu navegador para ver o fluxo completo com zonas ambientais e conectores.

---

## 3. Passo a Passo de Implementação

### Passo 1: Otimização do Dockerfile e Dependências

Antes de automatizar, garanta que a imagem de produção seja leve e não compile pacotes desnecessários:

1. **Separação de dependências:**
   - `requirements.txt`: Somente o essencial para rodar em produção. Use `-binary` para pacotes em C (ex.: `psycopg2-binary`).
   - `requirements-dev.txt`: Ferramentas de desenvolvimento e testes (`pytest`, `ipython`, `debugpy`, etc.).
2. **Uso de imagem Slim no Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   ENV PYTHONDONTWRITEBYTECODE=1 \
       PYTHONUNBUFFERED=1 \
       PIP_NO_CACHE_DIR=1

   # Instala dependências mínimas de sistema e limpa cache do apt
   RUN apt-get update && apt-get install -y --no-install-recommends \
       curl \
       && rm -rf /var/lib/apt/lists/*

   # Copia e instala requirements antes do código para aproveitar cache
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   WORKDIR /app/src
   EXPOSE 8000

   COPY start.sh /start.sh
   RUN chmod +x /start.sh

   ENTRYPOINT ["/start.sh"]
   CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

---

### Passo 2: Configuração do GitHub Actions

Crie o arquivo `.github/workflows/deploy.yml` na raiz do repositório:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - main
      - master
    paths-ignore:
      - 'README.md'
      - '.docs/**'
      - '.gitignore'

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=raw,value=latest
            type=sha,format=short

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Trigger Coolify Webhook
        env:
          COOLIFY_WEBHOOK_URL: ${{ secrets.COOLIFY_WEBHOOK_URL }}
        run: |
          if [ -n "$COOLIFY_WEBHOOK_URL" ]; then
            echo "Disparando redeploy no Coolify..."
            curl -f -X GET "$COOLIFY_WEBHOOK_URL"
          else
            echo "Aviso: COOLIFY_WEBHOOK_URL não configurado nos Secrets. Pulando disparo de webhook."
          fi
```

#### Habilitar permissão de escrita de pacotes no GitHub:
1. Acesse o repositório no GitHub: **Settings > Actions > General**.
2. Na seção **Workflow permissions**, selecione **"Read and write permissions"** e salve.

---

### Passo 3: Configuração da Aplicação no Coolify

No painel do Coolify:

1. **Criar Recurso por Imagem Docker:**
   - Em vez de escolher *Public/Private Repository*, clique em **+ New Resource > Docker Image**.
   - Defina o nome da imagem:
     ```text
     ghcr.io/<seu-usuario-github>/<nome-do-repo>:latest
     ```
2. **Para Repositórios Privados (Autenticação do GHCR):**
   - No GitHub: gere um token em **Settings > Developer Settings > Personal access tokens (Classic)** com permissão `read:packages`.
   - No Coolify: vá em **Sources / Registries > Add Registry**.
   - Escolha **GitHub Container Registry (`ghcr.io`)**, adicione seu username e o token criado.
3. **Configuração de Runtime:**
   - Configure as variáveis de ambiente normais da aplicação (`POSTGRES_HOST`, `JWT_SECRET`, etc.).
   - Defina a porta exposta (ex.: `8000`).
4. **Obter o Webhook de Deploy:**
   - Na página da aplicação no Coolify, role até a seção **Webhooks**.
   - Copie a URL do **Deploy Webhook** (exemplo: `https://coolify.seudominio.com/api/v1/deploy?uuid=...`).

---

### Passo 4: Configurar o Secret no GitHub

1. No repositório no GitHub: vá em **Settings > Secrets and variables > Actions**.
2. Clique em **New repository secret**:
   - **Name:** `COOLIFY_WEBHOOK_URL`
   - **Secret:** Cole a URL copiada no Coolify.

---

### Passo 5: Medida de Segurança no Servidor (SWAP de 4GB)

Mesmo sem rodar builds pesados, é uma **boa prática mandatória** garantir que a VPS tenha SWAP para absorver picos de uso e evitar travamento do SSH/Coolify:

Acesse o servidor via SSH e rode:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```
Verifique com:
```bash
free -h
```

---

## 4. Comparativo de Resultados

| Métrica | Build Local no Coolify | Build no GitHub Actions (GHCR) |
|---|---|---|
| **Tempo de Deploy** | 5 a 10 min (ou trava) | ~5 a 10 segundos |
| **Uso de CPU na VPS** | 200% (todos os núcleos) | < 5% |
| **Uso de RAM na VPS** | 100% (risco de OOM) | Apenas o runtime da aplicação |
| **Disponibilidade Coolify** | Fica inacessível durante build | 100% estável |
| **Rollback** | Recompilar commit antigo | Trocar a tag para a versão SHA anterior instantaneamente |
