from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from database import (
    create_server_connection,
    execute_read_query,
)
from domain.post_crud import get_post, create_new_post, PostRequest, get_post_list
from .auth import get_current_user

router = APIRouter(prefix="/api/post", tags=["posts"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/list")
def post_list():
    posts = get_post_list()
    return posts


@router.get("/detail/{post_id}")
def post_detail(post_id: int):
    post = get_post(post_id)
    return post


@router.post("/create")
def create_post(post_request: PostRequest, user: user_dependency):
    try:
        user_id = user.get("id")
        create_new_post(user_id, post_request)
        return {"message": "Post created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create post: {str(e)}")
