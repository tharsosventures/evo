import sqlite3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from domains.sql import parser, fitness


def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE numbers(value INTEGER)")
    conn.executemany("INSERT INTO numbers(value) VALUES(?)", [(i,) for i in range(100)])
    return conn


def test_parser_valid():
    conn = setup_db()
    assert parser.is_valid_sql("SELECT * FROM numbers", conn)
    assert not parser.is_valid_sql("SELEC FROM", conn)
    conn.close()


def test_fitness():
    conn = setup_db()
    cost = fitness.evaluate("SELECT SUM(value) FROM numbers", conn)
    assert cost >= 0
    conn.close()
