from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from domain.post_crud import (
    get_post,
    create_new_post,
    PostRequest,
    get_post_list,
    update_post,
    delete_post,
)
from .auth import get_current_user

router = APIRouter(prefix="/api/post", tags=["posts"])

user_dependency = Annotated[dict, Depends(get_current_user)]


class DeletePostRequest(BaseModel):
    post_id: int


@router.get("/list")
def post_list_api():
    posts = get_post_list()
    return posts


@router.get("/detail/{post_id}")
def post_detail_api(post_id: int):
    post = get_post(post_id)
    return post


@router.post("/create")
def create_post_api(post_request: PostRequest, user: user_dependency):
    try:
        user_id = user.get("id")
        create_new_post(user_id, post_request)
        return {"message": "Post created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create post: {str(e)}")


@router.put("/update/{post_id}")
def update_post_api(post_request: PostRequest, post_id: int):

    update_post(post_id, post_request)

    return {"detail": "Post updated successfully"}


@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_api(post_id: int):
    delete_post(post_id)

    return {"detail": "Post deleted successfully"}
