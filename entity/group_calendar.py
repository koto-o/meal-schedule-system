from datetime import date
from typing import Dict, Optional, List
from entity.user_calendar import UserCalendar
from entity.meal_schedule import MealSchedule

class GroupCalendar:
    def __init__(self, group_id: str, group_name: str):
        self.group_id = group_id
        self.group_name = group_name
        # ユーザーID (str) をキー、その人のUserCalendarオブジェクトを値とする辞書
        # 例: { "user_father": UserCalendarオブジェクト, "user_mother": UserCalendarオブジェクト }
        self.user_calendars: Dict[str, UserCalendar] = {}

    def add_user_calendar(self, user_calendar: UserCalendar):
        """グループにメンバーの個人カレンダーを紐付ける"""
        self.user_calendars[user_calendar.user_id] = user_calendar

    def get_member_schedule_by_date(self, user_id: str, target_date: date) -> Optional[MealSchedule]:
        """特定のメンバーの、特定の日付のスケジュールを取得する"""
        user_cal = self.user_calendars.get(user_id)
        if user_cal:
            return user_cal.get_schedule_by_date(target_date)
        return None

    def get_group_schedules_by_date(self, target_date: date) -> Dict[str, Optional[MealSchedule]]:
        """特定の日付の、家族全員のスケジュールをまとめて取得する（一覧表示用）"""
        group_status = {}
        for user_id, user_cal in self.user_calendars.items():
            group_status[user_id] = user_cal.get_schedule_by_date(target_date)
        return group_status


