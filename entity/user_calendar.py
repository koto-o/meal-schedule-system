from datetime import date
from typing import Dict, Optional
from entity.meal_schedule import MealSchedule

class UserCalendar:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # 日付 (date型) をキー、MealScheduleオブジェクトを値とする辞書
        # 例: { date(2026, 7, 5): MealScheduleオブジェクト }
        self.schedules: Dict[date, MealSchedule] = {}

    def add_or_update_schedule(self, schedule: MealSchedule):
        """カレンダーにスケジュールを追加または更新する"""
        if schedule.user_id != self.user_id:
            raise ValueError("このスケジュールは別のユーザーのものです。")
        
        self.schedules[schedule.target_date] = schedule

    def get_schedule_by_date(self, target_date: date) -> Optional[MealSchedule]:
        """指定された日付のスケジュールを取得する（なければNone）"""
        return self.schedules.get(target_date)

    def delete_schedule_by_date(self, target_date: date):
        """指定された日付のスケジュールを削除する"""
        if target_date in self.schedules:
            del self.schedules[target_date]


