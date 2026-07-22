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
            breakfast_message TEXT,
                       
            lunch_required INTEGER NOT NULL,
            lunch_message TEXT,
                       
            dinner_required INTEGER NOT NULL,
            dinner_message TEXT,
                       
            return_time TEXT,
                       
            UNIQUE(account_id, target_date)
        )
        """)

        conn.commit()
        conn.close()

    def get_schedule(self, account_id, target_date):

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                breakfast_required,
                breakfast_message,

                lunch_required,
                lunch_message,

                dinner_required,
                dinner_message,

                return_time
            FROM meal_schedules
            WHERE
                account_id=?
                AND target_date=?
        """,(account_id, target_date))


        row = cursor.fetchone()

        conn.close()


        if row is None:
            return None


        return {
            "breakfast": row[0],
            "breakfast_message": row[1] or "",

            "lunch": row[2],
            "lunch_message": row[3] or "",

            "dinner": row[4],
            "dinner_message": row[5] or "",

            "return_time": row[6] or ""
        }
    
    def get_group_schedule(self, group_id, target_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                users.user_name,
                meal_schedules.breakfast_required,
                meal_schedules.breakfast_message,
                       
                meal_schedules.lunch_required,
                meal_schedules.lunch_message,
                       
                meal_schedules.dinner_required,
                meal_schedules.dinner_message,
                       
                meal_schedules.return_time
                       
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
        breakfast_message,

        lunch_required,
        lunch_message,

        dinner_required,
        dinner_message,

        return_time
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
                    breakfast_message,
                           
                    lunch_required,
                    lunch_message,
                           
                    dinner_required,
                    dinner_message,
                           
                    return_time
                )
                VALUES(?,?,?,?,?,?,?,?,?)
            """,(
                account_id,
                target_date,

                breakfast_required,
                breakfast_message,

                lunch_required,
                lunch_message,
                
                dinner_required,
                dinner_message,

                return_time
            ))

        else:

            cursor.execute("""
            UPDATE meal_schedules
            SET
                breakfast_required=?,
                breakfast_message=?,

                lunch_required=?,
                lunch_message=?,

                dinner_required=?,
                dinner_message=?,

                return_time=?
            WHERE
                account_id=?
                AND target_date=?
            """,(
                breakfast_required,
                breakfast_message,

                lunch_required,
                lunch_message,

                dinner_required,
                dinner_message,

                return_time,

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
                breakfast_message,
                       
                lunch_required,
                lunch_message,
                       
                dinner_required,
                dinner_message,
                       
                return_time
                       
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
