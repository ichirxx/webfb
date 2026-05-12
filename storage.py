import os
import psycopg2
from psycopg2 import sql

_DB_URL = "postgresql://neondb_owner:npg_q0kcVZ19Utdx@ep-delicate-breeze-ap808hxk-pooler.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def _get_conn():
    return psycopg2.connect(_DB_URL)

def _ensure_table():
    try:
        conn = _get_conn()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS kv_store (
            name TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            data TEXT NOT NULL
        )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB ERROR:", e)

def save(table, key, value):
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO kv_store (name, data) VALUES (%s, %s)
    ON CONFLICT (name) DO UPDATE SET data = %s
    """, (key, str(value), str(value)))
    conn.commit()
    cur.close()
    conn.close()

def load(table, key, default=None):
    _ensure_table()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT data FROM kv_store WHERE name = %s", (key,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return eval(row[0])
    return de
    fault 

