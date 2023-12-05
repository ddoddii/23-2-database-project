import mysql.connector
import yaml
from mysql.connector import Error

with open("config/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
        print("MySQL Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred")
    return result
