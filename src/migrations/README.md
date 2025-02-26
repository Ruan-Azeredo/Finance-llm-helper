# Migrations

As migrations neste projeto são gerenciadas pelo pw-migrate (peewee-migrate).
As migrations devem garantir a equivalncia entre o banco de dados e os modelos no código. A baixão existem alguns comando guias e regras para lidar com as migrations neste projeto

1. Para cada alteração nas estruturas das tabelas existentes ou criação de alguma nova, deve ser criada ao menos uma migration que indique todas as alterações, afinal, o comando de migration ira rodar na build da aplicação e aas diffs entre as migrations e o banco de dados serão "migradas" para o banco de dados.

> Pode-se criar uma nova migration atravez:
>> Importante estar o diretorio src
```bash
pw-migrate create --database postgresql://postgres:postgres@0.0.0.0:5432/postgres [migration-name]
```
> Ao utilizar o comando --auto antes de --database serão reconhecidas as diffs automaticamente, mas CUIDADO! Este processo não é indicado uma vez que o pw-migrate tenta alterar mais campos do que deveria, como os campos datetime e as chaves estrangeiras.

2. Migrar as ou a migration. Faça a migração para a respectiva database local, e confira se as desejadas mudanças foram aplicada.

```bash
pw-migrate migrate --database postgresql://postgres:postgres@0.0.0.0:5432/postgres
```

> pode-se adicionar ao final do comnando, a migration especifica que deseja fazer a migração




https://github.com/klen/peewee_migrate