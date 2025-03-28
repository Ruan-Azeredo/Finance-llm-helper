from fastapi import Depends, HTTPException, status
from typing import Optional

from models import User, Transaction, Category, Month

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

def verify_only_self_access_category(current_user: User = Depends(User.get_current_user), category_id: Optional[str] = None) -> bool:
    
    category: Category = Category.from_id(category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category nao encontrada"
        )

    user: User = User.from_id(category.user_id)

    if current_user.role != "admin" and user.id is not None and current_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: não possui permissão para acessar esse dados de outro usuário"
        )

    return True

def verify_only_self_access_month(current_user: User = Depends(User.get_current_user), month_id: Optional[str] = None) -> bool:

    month: Month = Month.from_id(month_id)

    if month is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mês nao encontrado"
        )
    
    user: User = User.from_id(month.user_id)

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