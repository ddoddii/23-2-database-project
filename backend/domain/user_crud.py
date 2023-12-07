from database import create_server_connection, execute_single_read_query
from datetime import datetime
from pydantic import BaseModel


def get_user_id(username: str):
    connection = create_server_connection()

    query = "SELECT user_id FROM users WHERE username = %s;"
    user_id = execute_single_read_query(connection, query, (username,))

    connection.close()

    return user_id
