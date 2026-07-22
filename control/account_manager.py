import sqlite3, random
from entity.user import User

class AccountManager:
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()


    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                account_id INTEGER PRIMARY KEY,
                user_name TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def check_user_name_length(self, user_name):
        return 0 < len(user_name) <= 6

    def register_user(self, user_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        account_id = self.generate_account_id()

        cursor.execute(
            "INSERT INTO users (account_id, user_name) VALUES (?, ?)",
            (account_id, user_name)
        )
        conn.commit()
        conn.close()

        user =User(account_id, user_name)
        return user
  
    def has_user(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        conn.close()
        return count > 0
    
    def get_user(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT account_id, user_name
            FROM users
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return User(row[0], row[1])
    
    def generate_account_id(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        while True:
            account_id = random.randint(100000, 999999)

            cursor.execute(
                "SELECT account_id FROM users WHERE account_id = ?",
                (account_id,)
            )

            if cursor.fetchone() is None:
                conn.close()
                return account_id
            
    def delete_user(self, account_id):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM meal_schedules WHERE account_id = ?",
            (account_id,)
        )

        cursor.execute(
            "DELETE FROM group_members WHERE account_id = ?",
            (account_id,)
        )

        cursor.execute(
            "DELETE FROM users WHERE account_id = ?",
            (account_id,)
        )

        conn.commit()
        conn.close()

    def get_user_by_id(self, account_id):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT account_id,user_name
            FROM users
            WHERE account_id=?
        """,(account_id,))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return User(row[0],row[1])
