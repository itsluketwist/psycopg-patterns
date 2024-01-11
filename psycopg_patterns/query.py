import logging
from contextlib import contextmanager
from typing import Any, Callable, Generator

from psycopg import ClientCursor, Connection, Cursor, connect
from psycopg.rows import dict_row

from psycopg_patterns.configure import DatabaseVersion, get_conn_str


logger = logging.getLogger(__name__)


@contextmanager
def get_conn(
    conn_str: str | None = None,
    db_ver: DatabaseVersion | str | None = None,
    cur_type: Cursor = ClientCursor,
    row_type: Callable = dict_row,
) -> Generator[Connection, None, None]:
    """
    Create and provide a Connection object for the given database and cursor/row types.

    Parameters
    ----------
    conn_str: str | None = None
    db_ver: DatabaseVersion | str | None = None
    cur_type: Cursor = ClientCursor
    row_type: Callable = dict_row

    Returns
    -------
    Generator[Connection, None, None]
        Provides the standard context manager access to a psycopg Connection.
    """
    if conn_str is None:
        conn_str = get_conn_str(db_ver=db_ver)

    with connect(
        conn_str,
        cursor_factory=cur_type,
        row_factory=row_type,
    ) as conn:
        yield conn


def execute(
    query: str,
    params: dict[str, Any] | None = None,
) -> None:
    """
    Execute a query string with the given parameters, on the configured database.

    Parameters
    ----------
    query: str
    params: dict[str, Any] | None = None
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            logger.debug("EXECUTE - attempting query:\n%s", cur.mogrify(query, params))
            cur.execute(query, params)


def fetch_one(
    query: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Execute a query string with the given parameters (if any), returning a single record.

    Parameters
    ----------
    query: str
    params: dict[str, Any] | None = None

    Returns
    -------
    dict[str, Any] | None
        A single table record represented as a dictionary, or None if no output.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            logger.debug(
                "FETCH_ONE - attempting query:\n%s", cur.mogrify(query, params)
            )
            cur.execute(query, params)
            _val = cur.fetchone()

    return _val


def fetch_all(
    query: str,
    params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Execute a query string with the given parameters (if any), returning a list of records.

    Parameters
    ----------
    query: str
    params: dict[str, Any] | None = None

    Returns
    -------
    list[dict[str, Any]]
        A list of table records output from the query, represented as dictionaries.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            logger.debug(
                "FETCH_ALL - attempting query:\n%s", cur.mogrify(query, params)
            )
            cur.execute(query, params)
            _vals = cur.fetchall()

    return _vals


def select_all(
    table: str,
) -> list[dict[str, Any]]:
    """
    Simple query to get all records from the given table.

    Parameters
    ----------
    table: str

    Returns
    -------
    list[dict[str, Any]]
        All records in the table, represented as dictionaries.
    """
    return fetch_all(
        query=f"SELECT * FROM {table};",
    )
