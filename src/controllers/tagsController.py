from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from models import Tag
from schemas import TagCRUDInput
from .utilsController import *

tag_router = APIRouter()

tag_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])
tag_router_auth_by_tag = APIRouter(dependencies = [Depends(verify_only_self_access_tag)])
tag_router_admin = APIRouter(dependencies = [Depends(verify_admin_access_user)])

@tag_router_admin.get("/ops")
async def get_tags():

    tags: list[Tag] = Tag.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"tags": [tag.to_dict() for tag in tags]}
    )

@tag_router_auth.get("/from-user/{tag_id}")
async def get_tag_by_user_id(user_id: int):
    
    tags: list[Tag] = Tag.get_tags_by_user_id(user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"tags": [tag.to_dict() for tag in tags]}
    )

@tag_router_auth.post("/ops/{user_id}")
async def create_tag(user_id: int, tag_input: TagCRUDInput):

    tag: Tag = Tag.create(
        user_id = user_id,
        **tag_input.to_dict()
    )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Tag criada", "tag": tag.to_dict()}
    )

@tag_router_auth.post("/create-many-tags/{user_id}")
async def create_many_tags(user_id: int, tags_input: list[TagCRUDInput]):
        
    for tag_input in tags_input:
        Tag.create(
            user_id = user_id,
            **tag_input.to_dict()
        )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Tags criadas"}
    )

@tag_router_auth_by_tag.put("/ops/{tag_id}")
async def update_tag(tag_id: str, tag_input: TagCRUDInput):

    tag: Tag = Tag.from_id(tag_id)

    if not tag:
        raise HTTPException(status_code = 404, detail = "Tag não encontrada")
    
    tag.update(
        **tag_input.to_dict()
    )

    updated_tag: Tag = Tag.from_id(tag_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Tag atualizada", "tag": updated_tag.to_dict()}
    )

@tag_router_auth_by_tag.delete("/ops/{tag_id}")
async def delete_tag(tag_id: str):

    tag: Tag = Tag.from_id(tag_id)

    if not tag:
        raise HTTPException(status_code = 404, detail = "Tag não encontrada")
    
    tag.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Tag deletada"}
    )

tag_router.include_router(tag_router_auth)
tag_router.include_router(tag_router_auth_by_tag)
tag_router.include_router(tag_router_admin)