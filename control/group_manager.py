import sqlite3
from entity.group import Group


class GroupManager:
    def account_exists(self, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM users WHERE account_id = ?",
            (account_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS group_members (
                group_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def check_group_name_length(self, group_name):
        return 0 < len(group_name) <= 10

    def has_group(self, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM group_members WHERE account_id = ?",
            (account_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def create_group(self, account_id, group_name):
        if self.has_group(account_id):
            raise ValueError("既にグループに所属しています。")

        if not self.check_group_name_length(group_name):
            raise ValueError("グループ名は1～6文字で入力してください")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO groups (group_name) VALUES (?)",
            (group_name,)
        )

        group_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO group_members (group_id, account_id) VALUES (?, ?)",
            (group_id, account_id)
        )

        conn.commit()
        conn.close()

        return Group(group_id, group_name)

    def add_member(self, group_id, account_id):
        if not self.account_exists(account_id):
            raise ValueError("そのアカウントIDは存在しません。")

        if self.has_group(account_id):
            raise ValueError("このユーザーは既にグループに所属しています。")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO group_members (group_id, account_id) VALUES (?, ?)",
            (group_id, account_id)
        )

        conn.commit()
        conn.close()

    def remove_member(self, group_id, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM group_members WHERE group_id = ? AND account_id = ?",
            (group_id, account_id)
        )

        cursor.execute(
            "SELECT COUNT(*) FROM group_members WHERE group_id = ?",
            (group_id,)
        )

        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute(
                "DELETE FROM groups WHERE group_id = ?",
                (group_id,)
            )

        conn.commit()
        conn.close()
        
    def get_user_group_id(self, account_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT group_id FROM group_members WHERE account_id = ? LIMIT 1",
            (account_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return row[0]

    def get_group_name(self, group_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT group_name FROM groups WHERE group_id = ?",
            (group_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return row[0]
    
    def get_group_members(self, group_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT users.account_id, users.user_name
            FROM users
            JOIN group_members
                ON users.account_id = group_members.account_id
            WHERE group_members.group_id = ?
            ORDER BY users.user_name
        """, (group_id,))

        members = cursor.fetchall()

        conn.close()

        return members
