from datetime import datetime
from database import (
    create_server_connection,
    execute_single_read_query,
    execute_read_query,
)
import re
from pydantic import BaseModel
from typing import List
from domain.importance_crud import create_new_importance


class PostRequest(BaseModel):
    title: str
    content: str


def get_post_list():
    connection = create_server_connection()
    query = """
        SELECT * FROM POST
        ORDER BY created_time DESC;
        """
    posts = execute_read_query(connection, query)
    connection.close()
    return posts


def get_post(post_id: int):
    connection = create_server_connection()

    query = "SELECT * FROM post WHERE post_id = %s;"
    post = execute_single_read_query(connection, query, (post_id,))

    connection.close()

    return post


def create_new_post(user_id: int, create_post_request: PostRequest):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    # Current time for created_time
    now = datetime.now()

    importance_id = create_new_importance()

    # Insert post data into the post table
    post_query = """
    INSERT INTO post (author_id, importance_id, created_time, title, content)
    VALUES (%s, %s, %s, %s, %s);
    """
    post_values = (
        user_id,
        importance_id,
        now,
        create_post_request.title,
        create_post_request.content,
    )

    cursor.execute(post_query, post_values)
    post_id = cursor.lastrowid

    image_urls, video_urls = find_media_urls(create_post_request.content)

    for url in image_urls:
        image_query = """
        INSERT INTO image (post_id, image_url)
        VALUES (%s, %s);
        """
        cursor.execute(image_query, (post_id, url))

    for url in video_urls:
        video_query = """
        INSERT INTO video (post_id, video_url)
        VALUES (%s, %s);
        """
        cursor.execute(video_query, (post_id, url))

    connection.commit()
    cursor.close()
    connection.close()


def find_media_urls(content: str) -> (List[str], List[str]):
    # Regex for image URLs
    img_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:jpg|jpeg|png|gif)"
    # Regex for video URLs
    video_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:mp4|avi|mov)"

    img_urls = re.findall(img_pattern, content)
    video_urls = re.findall(video_pattern, content)

    return img_urls, video_urls
