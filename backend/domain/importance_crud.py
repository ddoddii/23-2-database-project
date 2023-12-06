from database import create_server_connection, execute_single_read_query
from datetime import datetime
import json


with open("config/parameters.json", "r") as f:
    config = json.load(f)


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


def get_importance_from_post(post_id: int):
    connection = create_server_connection()
    query = """
    SELECT * FROM post
    WHERE post_id = %s;
    """
    importance = execute_single_read_query(connection, query, (post_id,))
    return importance


def get_importance(importance_id: int):
    connection = create_server_connection()
    query = """
    SELECT * FROM importance
    WHERE importance_id = %s;
    """
    importance = execute_single_read_query(connection, query, (importance_id,))
    return importance


def get_post(post_id: int):
    connection = create_server_connection()

    query = "SELECT * FROM post WHERE post_id = %s;"
    post = execute_single_read_query(connection, query, (post_id,))

    connection.close()

    return post


def update_importance_score(post_id: int, day: int):
    connection = create_server_connection()
    post = get_post(post_id)
    view = post["view_count"]
    help = post["help_count"]
    importance_id = post["importance_id"]
    # Update new score based on view, help, day
    new_score = (
        view * config["viewWeight"] ^ day + help * config["clicksWeight"] ^ day
    ) * config["decayRate"] ^ day
    query = """
        UPDATE importance
        SET score = %s
        WHERE importance_id = %s;
        """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (new_score, importance_id))
    connection.commit()
    cursor.close()
    connection.close()


def check_score_under_threshold(score: int):
    if score < config["threshold"]:
        return True
    return False
