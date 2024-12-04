from fastapi import Depends, HTTPException, status
from typing import Optional

from models import User

def verify_only_self_access_user(current_user: User = Depends(User.get_current_user), user_id: Optional[int] = None) -> bool:

    if current_user.role != "admin" and user_id is not None and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: não possui permissão para acessar esse usuário"
        )

    return True

def verify_admin_access_user(current_user: User = Depends(User.get_current_user)) -> bool:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: nível de permissão insuficiente"
        )

    return True