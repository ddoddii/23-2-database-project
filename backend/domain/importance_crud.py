from database import create_server_connection
from datetime import datetime


def create_new_importance() -> int:
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    INSERT INTO importance (score, last_updated)
    VALUES (%s, %s);
    """

    cursor.execute(query, (0, datetime.now()))
    importance_id = cursor.lastrowid

    connection.commit()
    cursor.close()
    connection.close()

    return importance_id
