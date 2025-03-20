from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from models import Category
from schemas import CategoryCRUDInput
from .utilsController import *

category_router = APIRouter()

category_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])
category_router_auth_by_category = APIRouter(dependencies = [Depends(verify_only_self_access_category)])
category_router_admin = APIRouter(dependencies = [Depends(verify_admin_access_user)])

@category_router_admin.get("/ops")
async def get_categories():

    categories: list[Category] = Category.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"categories": [category.to_dict() for category in categories]}
    )

@category_router_auth.get("/from-user/{category_id}")
async def get_category_by_user_id(user_id: int):
    
    categories: list[Category] = Category.get_categories_by_user_id(user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"categories": [category.to_dict() for category in categories]}
    )

@category_router_auth.post("/ops/{user_id}")
async def create_category(user_id: int, category_input: CategoryCRUDInput):

    category: Category = Category.create(
        user_id = user_id,
        **category_input.to_dict()
    )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Category criada", "category": category.to_dict()}
    )

@category_router_auth.post("/create-many-categories/{user_id}")
async def create_many_categories(user_id: int, categories_input: list[CategoryCRUDInput]):
        
    for category_input in categories_input:
        Category.create(
            user_id = user_id,
            **category_input.to_dict()
        )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Categories criadas"}
    )

@category_router_auth_by_category.put("/ops/{category_id}")
async def update_category(category_id: str, category_input: CategoryCRUDInput):

    category: Category = Category.from_id(category_id)

    if not category:
        raise HTTPException(status_code = 404, detail = "Category não encontrada")
    
    category.update(
        **category_input.to_dict()
    )

    updated_category: Category = Category.from_id(category_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Category atualizada", "category": updated_category.to_dict()}
    )

@category_router_auth_by_category.delete("/ops/{category_id}")
async def delete_category(category_id: str):

    category: Category = Category.from_id(category_id)

    if not category:
        raise HTTPException(status_code = 404, detail = "Category não encontrada")
    
    category.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Category deletada"}
    )

category_router.include_router(category_router_auth)
category_router.include_router(category_router_auth_by_category)
category_router.include_router(category_router_admin)