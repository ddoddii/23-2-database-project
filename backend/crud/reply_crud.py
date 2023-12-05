from datetime import datetime
from database import create_server_connection, execute_query, execute_read_query
from routers.reply import AnswerCreate


def create_answer(request: AnswerCreate):
    connection = create_server_connection()
    cursor = connection.cursor()
    # Current time for created_time
    now = datetime.now()

    # Insert post data into the post table
    post_query = """
        INSERT INTO reply (post_id, author_id, importance_id, content, created_time, updated_time, help_count)
        VALUES (%s, %s, %s, %s, %s);
        """
    post_values = (
        user_id,
        author_id,
        importance_id,
        datetime.now(),
        datetime.now(),
        request.content,
        0,
    )

    cursor.execute(post_query, post_values)
