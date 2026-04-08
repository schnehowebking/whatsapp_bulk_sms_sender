import sqlite3
from config import DB_PATH
DB_NAME = DB_PATH


def init_db():

    with sqlite3.connect(DB_NAME) as conn:

        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        message TEXT,
        status TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS templates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        message TEXT
        )
        """)

        conn.commit()


def add_contact(name, phone):

    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()

            c.execute(
                "INSERT INTO contacts(name,phone) VALUES (?,?)",
                (name, phone)
            )

            conn.commit()

    except sqlite3.IntegrityError:
        pass


def get_contacts():

    with sqlite3.connect(DB_NAME) as conn:

        c = conn.cursor()

        c.execute("SELECT id,name,phone FROM contacts")

        return c.fetchall()


def add_log(phone, message, status):

    with sqlite3.connect(DB_NAME) as conn:

        c = conn.cursor()

        c.execute(
            "INSERT INTO logs(phone,message,status) VALUES (?,?,?)",
            (phone, message, status)
        )

        conn.commit()


def get_logs():

    with sqlite3.connect(DB_NAME) as conn:

        c = conn.cursor()

        c.execute("SELECT phone,message,status FROM logs ORDER BY id DESC")

        return c.fetchall()


def get_templates():

    with sqlite3.connect(DB_NAME) as conn:

        c = conn.cursor()

        c.execute("SELECT name,message FROM templates")

        return c.fetchall()