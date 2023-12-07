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


def update_reply(request, reply_id):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    # Update reply content
    query = """
                UPDATE reply
                SET  content = %s, updated_time = %s
                WHERE reply_id = %s;
                """
    cursor.execute(query, (request.content, datetime.now(), reply_id))
    connection.commit()
    cursor.close()
    connection.close()


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


def vote_reply(reply_id):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Update help_count in reply table
        update_query = """
        UPDATE reply
        SET help_count = help_count + 1
        WHERE reply_id = %s;
        """
        cursor.execute(update_query, (reply_id,))

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


def view_reply(post_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    # Update help_count in reply table
    update_query = """
        UPDATE reply
        SET view_count = view_count + 1
        WHERE post_id = %s;
        """
    cursor.execute(update_query, (post_id,))

    # Commit the transaction
    connection.commit()
    return True

    cursor.close()
    connection.close()


def delete_reply(reply_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)

    delete_replies_query = "DELETE FROM reply WHERE reply_id = %s;"
    cursor.execute(delete_replies_query, (reply_id,))
    connection.commit()
    cursor.close()
    connection.close()
