def authenticate_user(username, password, role):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND role = ?", (username, password, role))
        user = cursor.fetchone()
        if user:
            return True, {"id": user[0], "name": user[1]}
        return False, None
