"""
Raw Postgres connection using psycopg2.
Bypasses Django ORM — reads directly from gold schema views.
"""

import os
import json
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME",     "starrise_db"),
        user=os.getenv("DB_USER",       "starrise_user"),
        password=os.getenv("DB_PASSWORD","starrise_pass"),
        host=os.getenv("DB_HOST",       "localhost"),
        port=os.getenv("DB_PORT",       "5432"),
    )


def execute_query(sql: str, params: dict = None) -> list[dict]:
    """Execute a SQL query and return list of dicts."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or {})
            rows = cur.fetchall()
            # Parse any JSON strings returned from JSON_AGG
            result = []
            for row in rows:
                parsed = {}
                for key, val in row.items():
                    if isinstance(val, str) and (val.startswith("[") or val.startswith("{")):
                        try:
                            val = json.loads(val)
                        except Exception:
                            pass
                    parsed[key] = val
                result.append(parsed)
            return result
