from datetime import date, datetime
from typing import Optional

class MealSchedule:
    def __init__(self, schedule_id: str, user_id: str, target_date: date):
        self.schedule_id = schedule_id
        self.user_id = user_id            # 誰の予定か
        self.target_date = target_date    # 対象の日付
        
        # 食事が必要かどうか (True: いる, False: いらない, None: 未入力)
        self.needs_meal: Optional[bool] = None 
        
        # 帰宅時間 (例: "19:30" や datetime.time型 など。ここでは文字列かNone)
        self.return_time: Optional[str] = None 

    def update_meal_status(self, needs_meal: bool):
        """食事の要否を更新する"""
        self.needs_meal = needs_meal

    def update_return_time(self, return_time: Optional[str]):
        """帰宅時間を更新する"""
        self.return_time = return_time