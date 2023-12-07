from database import create_server_connection, execute_single_read_query
from datetime import datetime
from pydantic import BaseModel

from domain.importance_crud import create_new_importance


class ReplyRequest(BaseModel):
    content: str


class Reply(BaseModel):
    id: int
    content: str
    create_date: datetime


def get_post_reply(post_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM reply
    WHERE post_id = %s;
    """
    cursor.execute(query, (post_id,))
    replies = cursor.fetchall()
    connection.close()
    return replies


def get_reply(reply_id: int):
    connection = create_server_connection()

    query = "SELECT * FROM reply WHERE reply_id = %s;"
    reply = execute_single_read_query(connection, query, (reply_id,))

    connection.close()

    return reply


def create_new_reply(user_id: int, post_id: int, reply_request: ReplyRequest):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    now = datetime.now()
    importance_id = create_new_importance()

    reply_query = """
    INSERT INTO reply (post_id, author_id, importance_id, created_time,updated_time, content)
    VALUES (%s, %s, %s, %s, %s,  %s);
    """
    reply_values = (
        post_id,
        user_id,
        importance_id,
        now,
        now,
        reply_request.content,
    )
    cursor.execute(reply_query, reply_values)
    connection.commit()
    cursor.close()
    connection.close()
