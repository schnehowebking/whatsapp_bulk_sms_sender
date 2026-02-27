import sqlite3

DB_NAME = "whatsapp.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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

    conn.commit()
    conn.close()

def add_contact(name, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO contacts(name, phone) VALUES (?,?)", (name, phone))
        conn.commit()
    except:
        pass
    conn.close()

def get_contacts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id,name,phone FROM contacts")
    data = c.fetchall()
    conn.close()
    return data

def add_log(phone, message, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs(phone,message,status) VALUES (?,?,?)",
              (phone, message, status))
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT phone,status FROM logs ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data