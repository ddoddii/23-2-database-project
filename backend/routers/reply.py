from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from domain.reply_crud import create_new_reply, ReplyRequest
from .auth import get_current_user

router = APIRouter(prefix="/api/reply", tags=["reply"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create/{post_id}")
def create_reply(post_id: int, reply_request: ReplyRequest, user: user_dependency):
    try:
        user_id = user.get("id")
        create_new_reply(user_id, post_id, reply_request)
        return {"message": "Reply created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create post: {str(e)}")
