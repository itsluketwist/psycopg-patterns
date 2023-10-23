# **psycopg-patterns**


![check code workflow](https://github.com/itsluketwist/psycopg-patterns/actions/workflows/check.yaml/badge.svg)


<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://opensource.org/licenses/MIT">
        <img alt="MIT License" src="https://img.shields.io/badge/Licence-MIT-yellow?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3" src="https://img.shields.io/badge/Python_3-blue?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://www.psycopg.org/">
        <img alt="psycopg" src="https://img.shields.io/badge/psycopg-green?style=for-the-badge&logo=python&logoColor=white" />
    </a>
</div>

## *usage*

Contains some basic coding patterns / utils for when using the `psycopg` library...

First configure the connection string in your environment:

```shell
export PSYCOPG_PATTERNS_CONN_STR=postgresql://postgres:postgres@localhost:5432/database_name
```

Then import and use:

```python
import psycopg_patterns as db

result = db.fetch_one(
    query="""
        SELECT * FROM table_name
        WHERE id = %(id)s;
    """,
    params={"id": 1},
)
```

## *installation*

Install directly from GitHub, using pip:

```shell
pip install git+https://github.com/itsluketwist/psycopg-patterns
```

## *development*

Clone the repository code:

```shell
git clone https://github.com/itsluketwist/psycopg-patterns.git
```

Once cloned, install the package locally in a virtual environment:

```shell
python -m venv venv

. venv/bin/activate

pip install -e ".[dev]"
```

Install and use pre-commit to ensure code is in a good state:

```shell
pre-commit install

pre-commit autoupdate

pre-commit run --all-files
```

## *testing*

Run the test suite using:

```shell
pytest .
```


## *inspiration*

I found myself re-writing similar code every time I used `psycopg`, decided to package it up for myself.