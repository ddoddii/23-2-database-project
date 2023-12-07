import json
from datetime import datetime, timezone

from database import create_server_connection, execute_single_read_query

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
    SELECT post.importance_id FROM post
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


def update_all_post_importance_score():
    # 현재 시간
    now = datetime.now(timezone.utc)
    utc_now = now.astimezone(timezone.utc).replace(tzinfo=None)

    # 모든 게시글 목록 조회
    posts = get_all_posts()
    # 각 게시글의 중요도 갱신
    for post in posts:
        utc_created_time = (
            post["created_time"].astimezone(timezone.utc).replace(tzinfo=None)
        )
        days = (utc_now - utc_created_time).days
        update_importance_score(post["post_id"], days)


def update_importance_score(post_id: int, days: int):
    connection = create_server_connection()
    now = datetime.now()
    post = get_post(post_id)
    view = post["view_count"]
    help = post["help_count"]
    importance_id = post["importance_id"]
    # Update new score based on view, help, day
    day = days % int(config["decayPeriod"])
    new_score = (
        view * float(config["viewsWeight"]) ** day
        + help * float(config["clicksWeight"]) ** day
    ) * float(config["decayRate"]) ** day
    query = """
        UPDATE importance
        SET score = %s, last_updated = %s
        WHERE importance_id = %s;
        """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (round(new_score, 2), now, importance_id))
    connection.commit()
    cursor.close()
    connection.close()


def check_score_under_threshold(score: int):
    if score < config["threshold"]:
        return True
    return False


def get_all_posts():
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
                SELECT post.post_id, post.importance_id,post.created_time, DATEDIFF(NOW(), created_time) AS day
                FROM post
                ORDER BY post.created_time DESC;
                """
    cursor.execute(query)
    posts = cursor.fetchall()
    cursor.close()
    connection.close()
    return posts


def delete_post(post_id: int):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM post WHERE post_id = %s;"
    cursor.execute(query, (post_id,))
    connection.commit()
    cursor.close()
    connection.close()
