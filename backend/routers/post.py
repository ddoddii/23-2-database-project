from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

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


@router.put("/update/{post_id}")
def update_post(post_request: PostRequest, user: user_dependency, post_id: int):
    user_id = user.get("id")
    post = get_post(post_id)
    if post["author_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to delete this post",
        )
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    # Update post title / content
    query = """
        UPDATE post
        SET title = %s, content = %s
        WHERE post_id = %s;
        """
    cursor.execute(query, (post_request.title, post_request.content, post_id))
    connection.commit()
    cursor.close()
    connection.close()

    return {"detail": "Post updated successfully"}


@router.delete("/delete")
def delete_post(post_id: int, user: user_dependency):
    user_id = user.get("id")
    post = get_post(post_id)
    if post["author_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to delete this post",
        )
    connection = create_server_connection()

    # Delete the post
    cursor = connection.cursor()
    query = "DELETE FROM post WHERE post_id = %s;"
    cursor.execute(query, (post_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return {"detail": "Post deleted successfully"}
