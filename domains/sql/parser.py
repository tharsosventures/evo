import sqlite3


def is_valid_sql(query: str, conn: sqlite3.Connection | None = None) -> bool:
    """Check SQL validity using SQLite's parser."""
    temp_conn = conn is None
    if conn is None:
        conn = sqlite3.connect(":memory:")
    try:
        conn.execute(f"EXPLAIN {query}")
        return True
    except sqlite3.Error:
        return False
    finally:
        if temp_conn:
            conn.close()


def prettify(query: str) -> str:
    """Very small prettifier: collapse whitespace."""
    return " ".join(query.strip().split())
