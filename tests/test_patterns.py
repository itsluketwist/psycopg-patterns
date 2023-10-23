import psycopg_patterns as db
from tests.conftest import TEST_DATABASE, TEST_PASSWORD, TEST_USERNAME


def test_patterns(create_db):
    """Simple test to check the main functionality works correctly."""
    # test set up
    test_table_name = "pscyopg_patterns_test_table"
    db.configure_conn_str(
        conn_str=db.build_conn_str(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            hostname="localhost",
            db_name=TEST_DATABASE,
        ),
    )

    # create the table directly
    db.execute(
        query=f"""
            CREATE TABLE {test_table_name} (
                id INT,
                name VARCHAR(255)
            );
        """,
    )

    # add some values
    db.execute(
        query=f"""
            INSERT INTO {test_table_name} (id, name)
            VALUES (1, 'hello'), (2, 'world');
        """,
    )

    # simple general query to test parameters and fetch_one
    query_one = f"SELECT * FROM {test_table_name} WHERE id=%(id)s;"

    # query single row that exists
    record = db.fetch_one(query=query_one, params={"id": 1})
    assert record == {"id": 1, "name": "hello"}

    # query single row that does not exist
    record = db.fetch_one(query=query_one, params={"id": 3})
    assert record is None

    # get all records and check them
    records = db.select_all(table=test_table_name)
    assert len(records) == 2
    assert sorted(records, key=lambda x: x["id"]) == [
        {"id": 1, "name": "hello"},
        {"id": 2, "name": "world"},
    ]
