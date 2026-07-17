import sqlite3


class MealScheduleManager:
    def __init__(self):
        self.db_name = "meal_schedule.db"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            target_date TEXT NOT NULL,
            breakfast_required INTEGER NOT NULL,
            lunch_required INTEGER NOT NULL,
            dinner_required INTEGER NOT NULL,
            return_time TEXT,
            message TEXT,
            UNIQUE(account_id, target_date)
        )
        """)

        conn.commit()
        conn.close()

    def set_one_meal_schedule(self, account_id, target_date, meal_type, required, return_time, message):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO meal_schedules (
                account_id, target_date, meal_type, required, return_time, message
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            account_id,
            target_date,
            meal_type,
            int(required),
            return_time,
            message
        ))

        conn.commit()
        conn.close()

    def get_schedule(self, account_id, target_date):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                breakfast_required,
                lunch_required,
                dinner_required,
                return_time,
                message
            FROM meal_schedules
            WHERE
                account_id=?
                AND target_date=?
        """,(account_id,target_date))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return {
            "breakfast": row[0],
            "lunch": row[1],
            "dinner": row[2],
            "return_time": row[3] or "",
            "message": row[4] or ""
        }
    
    def get_group_schedule(self, group_id, target_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                users.user_name,
                meal_schedules.breakfast_required,
                meal_schedules.lunch_required,
                meal_schedules.dinner_required,
                meal_schedules.return_time,
                meal_schedules.message
            FROM meal_schedules
            JOIN users
                ON meal_schedules.account_id = users.account_id
            JOIN group_members
                ON users.account_id = group_members.account_id
            WHERE
                group_members.group_id = ?
                AND meal_schedules.target_date = ?
            ORDER BY
                users.user_name
        """, (group_id, target_date))

        schedules = cursor.fetchall()

        conn.close()

        return schedules
    
    def set_schedule(
        self,
        account_id,
        target_date,
        breakfast_required,
        lunch_required,
        dinner_required,
        return_time,
        message
    ):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT schedule_id
            FROM meal_schedules
            WHERE account_id=? AND target_date=?
        """, (account_id, target_date))

        row = cursor.fetchone()

        if row is None:

            cursor.execute("""
                INSERT INTO meal_schedules(
                    account_id,
                    target_date,
                    breakfast_required,
                    lunch_required,
                    dinner_required,
                    return_time,
                    message
                )
                VALUES(?,?,?,?,?,?,?)
            """,(
                account_id,
                target_date,
                int(breakfast_required),
                int(lunch_required),
                int(dinner_required),
                return_time,
                message
            ))

        else:

            cursor.execute("""
                UPDATE meal_schedules
                SET
                    breakfast_required=?,
                    lunch_required=?,
                    dinner_required=?,
                    return_time=?,
                    message=?
                WHERE
                    account_id=?
                    AND target_date=?
            """,(
                int(breakfast_required),
                int(lunch_required),
                int(dinner_required),
                return_time,
                message,
                account_id,
                target_date
            ))

        conn.commit()
        conn.close()

    def get_user_schedule(self, account_id, target_date):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                users.user_name,
                breakfast_required,
                lunch_required,
                dinner_required,
                return_time,
                message
            FROM meal_schedules
            JOIN users
            ON meal_schedules.account_id=users.account_id
            WHERE
                meal_schedules.account_id=?
                AND target_date=?
        """,(account_id,target_date))

        schedules = cursor.fetchall()

        conn.close()

        return schedules
