import re
from datetime import datetime
from typing import List

from pydantic import BaseModel

from database import (
    create_server_connection,
    execute_single_read_query,
    execute_read_query,
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
        SELECT post.post_id, post.title, post.content, post.created_time, post.updated_time,post.view_count, post.help_count, users.username
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
        SELECT post.post_id, post.title, post.content, post.created_time, post.updated_time,post.view_count, post.help_count, users.username
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
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT post.post_id, post.author_id, post.importance_id, post.title, post.content, post.created_time, post.updated_time, post.view_count, post.help_count, users.username
    FROM post 
    JOIN users ON post.author_id = users.user_id
    WHERE post_id = %s;
    """
    cursor.execute(query, (post_id,))
    post = cursor.fetchone()

    # Reply for that post
    replies_query = """
    SELECT reply_id, author_id, importance_id, content, created_time, updated_time, 
           help_count, view_count,  users.username
    FROM reply
    JOIN users ON reply.author_id = users.user_id
    WHERE post_id = %s;
    """
    cursor.execute(replies_query, (post_id,))
    replies = cursor.fetchall()
    connection.close()

    post_info = {
        "post_id": post["post_id"],
        "author_id": post["author_id"],
        "importance_id": post["importance_id"],
        "title": post["title"],
        "content": post["content"],
        "created_time": post["created_time"],  # format datetime
        "updated_time": post["updated_time"],
        "view_count": post["view_count"],
        "help_count": post["help_count"],
        "username": post["username"],
        "answers": replies,  # include replies as nested list
    }

    return post_info


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

    delete_replies_query = "DELETE FROM reply WHERE post_id = %s;"
    cursor.execute(delete_replies_query, (post_id,))
    connection.commit()

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
    connection.commit()
    cursor.close()
    connection.close()


def vote_post(post_id):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    try:
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
