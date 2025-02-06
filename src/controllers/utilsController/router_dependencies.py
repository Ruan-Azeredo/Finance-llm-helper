from fastapi import Depends, HTTPException, status
from typing import Optional

from models import User, Transaction, Tag

def verify_only_self_access_user(current_user: User = Depends(User.get_current_user), user_id: Optional[int] = None) -> bool:

    if current_user.role != "admin" and user_id is not None and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: não possui permissão para acessar esse dados de outro usuário"
        )

    return True

def verify_only_self_access_transaction(current_user: User = Depends(User.get_current_user), transaction_id: Optional[str] = None) -> bool:

    transaction: Transaction = Transaction.from_id(transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transação nao encontrada"
        )

    user: User = User.from_id(transaction.user_id)

    if current_user.role != "admin" and user.id is not None and current_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: não possui permissão para acessar esse dados de outro usuário"
        )

    return True

def verify_only_self_access_tag(current_user: User = Depends(User.get_current_user), tag_id: Optional[str] = None) -> bool:
    
        tag: Tag = Tag.from_id(tag_id)
    
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag nao encontrada"
            )
    
        user: User = User.from_id(tag.user_id)
    
        if current_user.role != "admin" and user.id is not None and current_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado: não possui permissão para acessar esse dados de outro usuário"
            )
    
        return True

def verify_admin_access_user(current_user: User = Depends(User.get_current_user)) -> bool:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: nível de permissão insuficiente"
        )

    return True