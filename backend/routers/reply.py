from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from domain.reply_crud import (
    create_new_reply,
    get_reply,
    update_reply,
    vote_reply,
    view_reply,
    delete_reply,
)
from .auth import get_current_user
from .post import ViewPostRequest

router = APIRouter(prefix="/api/reply", tags=["reply"])

user_dependency = Annotated[dict, Depends(get_current_user)]


class ReplyRequest(BaseModel):
    content: str


class VoteRequest(BaseModel):
    reply_id: int


@router.post("/create/{post_id}")
def create_reply(post_id: int, reply_request: ReplyRequest, user: user_dependency):
    try:
        user_id = user.get("id")
        create_new_reply(user_id, post_id, reply_request)
        return {"message": "Reply created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create post: {str(e)}")


@router.get("/detail/{reply_id}")
def reply_detail_api(reply_id: int):
    reply = get_reply(reply_id)
    return reply


@router.put("/update/{reply_id}")
def update_reply_api(request: ReplyRequest, reply_id: int):
    update_reply(request, reply_id)


@router.post("/vote")
def reply_vote_api(request: VoteRequest):
    vote_reply(request.reply_id)


@router.post("/view")
def reply_view_api(request: ViewPostRequest):
    view_reply(request.post_id)


@router.delete("/delete/{reply_id}")
def delete_reply_api(reply_id: int):
    try:
        delete_reply(reply_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update reply: {str(e)}")

    return {"detail": "reply deleted successfully"}
