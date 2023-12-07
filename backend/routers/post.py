from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status

from domain.importance_crud import (
    get_importance,
    update_all_post_importance_score,
)
from domain.post_crud import (
    get_post,
    create_new_post,
    PostRequest,
    get_post_list,
    update_post,
    delete_post,
    vote_post,
    view_post,
)
from .auth import get_current_user

router = APIRouter(prefix="/api/post", tags=["posts"])

user_dependency = Annotated[dict, Depends(get_current_user)]


class DeletePostRequest(BaseModel):
    post_id: int


class VotePostRequest(BaseModel):
    post_id: int


class ViewPostRequest(BaseModel):
    post_id: int


@router.get("/list")
def post_list_api(keyword: str = ""):
    posts = get_post_list(keyword=keyword)
    return posts


@router.get("/detail/{post_id}")
def post_detail_api(post_id: int):
    post = get_post(post_id)
    return post


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_post_api(post_request: PostRequest, user: user_dependency):
    try:
        user_id = user.get("id")
        create_new_post(user_id, post_request)
        return {"message": "Post created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create post: {str(e)}")


@router.put("/update/{post_id}")
def update_post_api(post_request: PostRequest, post_id: int, user: user_dependency):
    try:
        user_id = user.get("id")
        post = get_post(post_id)
        if post["author_id"] != user_id:
            raise HTTPException(status_code=401, detail="Not Authorized to update post")
        update_post(post_id, post_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update post: {str(e)}")

    return {"detail": "Post updated successfully"}


@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_api(post_id: int, user: user_dependency):
    try:
        user_id = user.get("id")
        post = get_post(post_id)
        if post["author_id"] != user_id:
            raise HTTPException(status_code=401, detail="Not Authorized to delete post")
        delete_post(post_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update post: {str(e)}")

    return {"detail": "Post deleted successfully"}


@router.post("/vote")
def post_vote_api(request: VotePostRequest, user: user_dependency):
    user_id = user.get("id")
    vote_post(user_id, request.post_id)


@router.post("/view")
def post_view_api(request: ViewPostRequest):
    view_post(request.post_id)


@router.post("/importance_score")
def view_importance_score_api():
    update_all_post_importance_score()
