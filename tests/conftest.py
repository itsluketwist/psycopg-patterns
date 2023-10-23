import os

import pytest

import psycopg_patterns as db


TEST_USERNAME = os.environ.get(
    "PSYCOPG_PATTERNS_DB_USERNAME",
    "postgres",
)
TEST_PASSWORD = os.environ.get(
    "PSYCOPG_PATTERNS_DB_PASSWORD",
    "postgres",
)
TEST_DATABASE = os.environ.get(
    "PSYCOPG_PATTERNS_TEST_DB_NAME",
    "psycopg_patterns_test_db",
)


@pytest.fixture(scope="session", autouse=True)
def create_db():
    base_db_conn = db.build_conn_str(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
        hostname="localhost",
        db_name="postgres",
    )

    # create the testing database
    with db.get_conn(conn_str=base_db_conn) as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query=f"DROP DATABASE IF EXISTS {TEST_DATABASE};")
        cur.execute(query=f"CREATE DATABASE {TEST_DATABASE};")

    # allow testing to happen
    yield

    # remove the testing database
    with db.get_conn(conn_str=base_db_conn) as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query=f"DROP DATABASE IF EXISTS {TEST_DATABASE};")
