import os

import mysql.connector
from dotenv import load_dotenv


class DBException(Exception):
    pass


def connect_db() -> mysql.connector.MySQLConnection:
    load_dotenv()
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_DATABASE")

    if None in [host, user, password, database]:
        raise DBException("Missing database credentials")

    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin="mysql_native_password",
        )  # type: ignore

    except mysql.connector.Error as err:
        raise DBException("Could not connect to database") from err
