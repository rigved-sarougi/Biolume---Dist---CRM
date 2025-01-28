import sqlite3

def connect_db():
    return sqlite3.connect("salon_b2b.db")

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                distributor TEXT,
                product_name TEXT,
                quantity INTEGER,
                status TEXT DEFAULT 'Pending',
                remarks TEXT
            )
        """)
        conn.commit()

def add_user(name, username, password, role):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)", (name, username, password, role))
        conn.commit()

def fetch_users(role=None):
    with connect_db() as conn:
        cursor = conn.cursor()
        if role:
            cursor.execute("SELECT username FROM users WHERE role = ?", (role,))
        else:
            cursor.execute("SELECT username FROM users")
        return [row[0] for row in cursor.fetchall()]

def add_order(distributor, product_name, quantity):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (distributor, product_name, quantity) VALUES (?, ?, ?)", (distributor, product_name, quantity))
        conn.commit()

def fetch_orders(username=None):
    with connect_db() as conn:
        cursor = conn.cursor()
        if username:
            cursor.execute("SELECT * FROM orders WHERE distributor = ?", (username,))
        else:
            cursor.execute("SELECT * FROM orders")
        return cursor.fetchall()

def update_order_status(order_id, status, remarks):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ?, remarks = ? WHERE id = ?", (status, remarks, order_id))
        conn.commit()
