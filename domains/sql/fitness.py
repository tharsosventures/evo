import sqlite3
from time import perf_counter
from . import parser


def evaluate(query: str, conn: sqlite3.Connection) -> float:
    """Return runtime of query in seconds; invalid SQL gets infinite cost."""
    if not parser.is_valid_sql(query, conn):
        return float("inf")
    start = perf_counter()
    try:
        conn.execute(query).fetchall()
    except sqlite3.Error:
        return float("inf")
    end = perf_counter()
    return end - start
