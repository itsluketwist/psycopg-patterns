import logging
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, List, Optional, Union

from psycopg import ClientCursor, Connection, Cursor, connect
from psycopg.rows import dict_row

from src.configure import DatabaseVersion, get_conn_str


logger = logging.getLogger(__name__)


@contextmanager
def get_conn(
    conn_str: Optional[str] = None,
    db_ver: Optional[Union[DatabaseVersion, str]] = None,
    cur_type: Cursor = ClientCursor,
    row_type: Callable = dict_row,
) -> Generator[Connection, None, None]:
    """
    Create and provide a Connection object for the given database and cursor/row types.

    Parameters
    ----------
    conn_str : Optional[str] = None
    db_ver : Optional[Union[DatabaseVersion, str]] = None
    cur_type : Cursor = ClientCursor
    row_type : Callable = dict_row

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
    params: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Execute a query string with the given parameters, on the configured database.

    Parameters
    ----------
    query : str
    params : Optional[Dict[str, Any]] = None
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            logger.debug("EXECUTE - attempting query:\n%s", cur.mogrify(query, params))
            cur.execute(query, params)


def fetch_one(
    query: str,
    params: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Execute a query string with the given parameters (if any), returning a single record.

    Parameters
    ----------
    query : str
    params : Optional[Dict[str, Any]] = None

    Returns
    -------
    Optional[Dict[str, Any]]
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
    params: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Execute a query string with the given parameters (if any), returning a list of records.

    Parameters
    ----------
    query : str
    params : Optional[Dict[str, Any]] = None

    Returns
    -------
    List[Dict[str, Any]]
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
) -> List[Dict[str, Any]]:
    """
    Simple query to get all records from the given table.

    Parameters
    ----------
    table : str

    Returns
    -------
    List[Dict[str, Any]]
        All records in the table, represented as dictionaries.
    """
    return fetch_all(
        query=f"SELECT * FROM {table};",
    )
