import logging
import os
from enum import Enum


logger = logging.getLogger(__name__)


PSYCOPG_PATTERNS_DB_VER = "PSYCOPG_PATTERNS_DB_VER"
PSYCOPG_PATTERNS_CONN_STR = "PSYCOPG_PATTERNS_CONN_STR"
PSYCOPG_PATTERNS_CONN_STR_DB = "PSYCOPG_PATTERNS_CONN_STR_{db}"


class DatabaseVersion(Enum):
    """Common database version names for use in configuration."""

    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


def build_conn_str(
    username: str,
    password: str,
    hostname: str,
    db_name: str,
    port: int = 5432,
    adapter: str = "postgresql",
) -> str:
    """
    Build a valid database connection url string from the provided parameters.

    Parameters
    ----------
    username : str
    password : str
    hostname : str
    port : int
    db_name : str
    adapter : str = "postgresql"

    Returns
    -------
    str
        The database connection url string.
    """
    return f"{adapter}://{username}:{password}@{hostname}:{port}/{db_name}"


def configure_db_ver(
    db_ver: DatabaseVersion | str,
) -> None:
    """
    Set the environment variable that determines which database version to use.

    Parameters
    ----------
    db_ver : DatabaseVersion | str
    """
    os.environ[PSYCOPG_PATTERNS_DB_VER] = str(db_ver)
    logger.debug(
        "Environment variable configured: %s=%s", PSYCOPG_PATTERNS_DB_VER, str(db_ver)
    )


def configure_conn_str(
    conn_str: str,
    db_ver: DatabaseVersion | str | None = None,
) -> None:
    """
    Set the environment variable that determines which database version to use.

    Parameters
    ----------
    conn_str : str
    db_ver : DatabaseVersion | str | None = None
    """
    if db_ver is None:
        # configure the default connection string
        _var_to_configure = PSYCOPG_PATTERNS_CONN_STR
    else:
        # otherwise configure the specified version
        _var_to_configure = PSYCOPG_PATTERNS_CONN_STR_DB.format(db=db_ver)

    os.environ[_var_to_configure] = conn_str
    logger.debug("Environment variable configured: %s=%s", _var_to_configure, conn_str)


def get_conn_str(
    db_ver: DatabaseVersion | str | None = None,
) -> str:
    """
    Get the database connection string that has been configured via environment variables.

    Parameters
    ----------
    db_ver : DatabaseVersion | str | None = None

    Returns
    -------
    str
        The database connection url string.
    """
    # if db not given, get the env var
    if db_ver is None:
        db_ver = os.getenv(PSYCOPG_PATTERNS_DB_VER)

    if db_ver is None:
        # if db_ver is still not provided, use the default
        return os.environ[PSYCOPG_PATTERNS_CONN_STR]
    else:
        # otherwise access the specified version
        return os.environ[PSYCOPG_PATTERNS_CONN_STR_DB.format(db=db_ver)]
