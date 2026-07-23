from flask import Flask, render_template_string, request, url_for

app = Flask(__name__)

# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyMealScheduleManager:
    def get_schedule(self, account_id: int, target_date: str, meal_type: str):
        """テスト用のダミーデータを返すメソッド"""
        # テスト用に「朝食は未登録」「昼食は不要」「夕食は必要」のシミュレーションデータ
        if meal_type == "breakfast":
            return None
        elif meal_type == "lunch":
            return {"required": False, "return_time": "", "message": ""}
        elif meal_type == "dinner":
            return {"required": True, "return_time": "19:30", "message": "遅れます"}
        return None

# マネージャーのインスタンス化
meal_schedule_manager = DummyMealScheduleManager()


# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日付詳細予定</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 25px; border-radius: 10px; max-width: 450px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 20px; margin-bottom: 20px; color: #333; }
        .meal-row { display: flex; align-items: center; justify-content: space-between; background-color: #f8f9fa; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #e9ecef; }
        .btn-meal { width: 80px; padding: 8px 0; background-color: #007bff; color: white; border: none; border-radius: 4px; font-weight: bold; text-decoration: none; font-size: 14px; text-align: center; }
        .btn-meal:hover { background-color: #0056b3; }
        .status-text { flex-grow: 1; text-align: left; margin-left: 15px; font-size: 14px; color: #495057; word-break: break-all; }
        .unregistered { color: #adb5bd; font-style: italic; }
        .btn-back { display: inline-block; width: 100%; padding: 12px; background-color: #6c757d; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>{{ target_date }} の予定</h2>
        
        {% for row in meal_rows %}
        <div class="meal-row">
            <a href="/meal-input?date={{ target_date }}&type={{ row.type }}" class="btn-meal">
                {{ row.name }}
            </a>
            <div class="status-text">
                {% if row.schedule is none %}
                    <span class="unregistered">未登録</span>
                {% else %}
                    <strong>{{ "必要" if row.schedule.required else "不要" }}</strong>
                    {% if row.schedule.required %}
                        <br><small>🕒 帰宅時間: {{ row.schedule.return_time or "-" }}</small>
                        <br><small>💬 伝言: {{ row.schedule.message or "-" }}</small>
                    {% endif %}
                {% endif %}
            </div>
        </div>
        {% endfor %}
        
        <a href="/calendar-placeholder" class="btn-back">カレンダーに戻る</a>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（一覧表示処理）
# ==========================================
@app.route('/date-detail')
def date_detail_view():
    # 本来はメインカレンダー画面から選択された日付を受け取る（テスト用に現在の日付を初期値に）
    target_date = request.args.get('date', '2026-07-10')
    account_id = 1  # 元コードの固定値

    # 朝食・昼食・夕食のデータをマネージャーから取得してリストにまとめる
    meal_types = [
        {"type": "breakfast", "name": "朝食"},
        {"type": "lunch", "name": "昼食"},
        {"type": "dinner", "name": "夕食"}
    ]
    
    meal_rows = []
    for meal in meal_types:
        schedule = meal_schedule_manager.get_schedule(account_id, target_date, meal["type"])
        meal_rows.append({
            "type": meal["type"],
            "name": meal["name"],
            "schedule": schedule
        })

    return render_template_string(HTML_TEMPLATE, target_date=target_date, meal_rows=meal_rows)


# ダミーの遷移先ルート（テスト用）
@app.route('/meal-input')
def meal_input_placeholder():
    date = request.args.get('date')
    meal_type = request.args.get('type')
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h2>（ここは meal_input_view 画面のダミーです）</h2>
        <p>受け取ったデータ -> 日付: {date} / 食事タイプ: {meal_type}</p>
        <a href="/date-detail?date={date}">一覧へ戻る</a>
    </div>
    """

@app.route('/calendar-placeholder')
def calendar_placeholder():
    return "<h3>ここはメインカレンダー画面（仮）です</h3><a href='/date-detail'>7月10日の詳細を見る</a>"


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)