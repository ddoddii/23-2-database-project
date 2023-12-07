import re
from datetime import datetime
from typing import List

from pydantic import BaseModel

from database import (
    create_server_connection,
    execute_single_read_query,
)
from domain.importance_crud import create_new_importance


class PostRequest(BaseModel):
    title: str
    content: str


def get_post_list(keyword: str = ""):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)

    if keyword:
        search = "%%{}%%".format(keyword)
        query = """
        SELECT post.post_id, post.title, post.content, post.created_time, post.updated_time, users.username
        FROM post
        JOIN users ON post.author_id = users.user_id
        WHERE post.title LIKE %s OR
              post.content LIKE %s OR
              users.username LIKE %s
        ORDER BY post.created_time DESC;
        """
        cursor.execute(query, (search, search, search))
    else:
        query = """
        SELECT post.post_id, post.title, post.content, post.created_time, post.updated_time, users.username
        FROM post
        JOIN users ON post.author_id = users.user_id
        ORDER BY post.created_time DESC;
        """
        cursor.execute(query)

    posts = cursor.fetchall()
    cursor.close()
    connection.close()

    return posts


def get_post(post_id: int):
    connection = create_server_connection()

    query = """
    SELECT post.post_id, post.author_id, post.importance_id, post.title, post.content, post.created_time, post.updated_time, post.view_count, post.help_count, users.username
    FROM post 
    JOIN users ON post.author_id = users.user_id
    WHERE post_id = %s;
    """
    post = execute_single_read_query(connection, query, (post_id,))

    connection.close()

    return post


def update_post(post_id: int, post_request: PostRequest):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    # Update post title / content
    query = """
            UPDATE post
            SET title = %s, content = %s, updated_time = %s
            WHERE post_id = %s;
            """
    cursor.execute(
        query, (post_request.title, post_request.content, datetime.now(), post_id)
    )
    connection.commit()
    cursor.close()
    connection.close()


def delete_post(post_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM post WHERE post_id = %s;"
    cursor.execute(query, (post_id,))
    connection.commit()
    cursor.close()
    connection.close()


def create_new_post(user_id, create_post_request: PostRequest):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    now = datetime.now()

    importance_id = create_new_importance()

    # Insert post data into the post table
    post_query = """
    INSERT INTO post (author_id, importance_id, created_time, updated_time, title, content)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    post_values = (
        user_id,
        importance_id,
        now,
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


def vote_post(user_id, post_id):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Insert into post_voter table
        insert_query = """
        INSERT INTO post_voter (post_id, user_id)
        VALUES (%s, %s);
        """
        cursor.execute(insert_query, (post_id, user_id))

        # Update help_count in post table
        update_query = """
        UPDATE post
        SET help_count = help_count + 1
        WHERE post_id = %s;
        """
        cursor.execute(update_query, (post_id,))

        # Commit the transaction
        connection.commit()
        return True

    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print(f"An error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def view_post(post_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Update help_count in post table
        update_query = """
            UPDATE post
            SET view_count = view_count + 1
            WHERE post_id = %s;
            """
        cursor.execute(update_query, (post_id,))

        # Commit the transaction
        connection.commit()
        return True

    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        print(f"An error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()
