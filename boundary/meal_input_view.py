from flask import Flask, render_template_string, request, redirect, url_for
# 本来は control.meal_schedule_manager からインポートします
# from control.meal_schedule_manager import MealScheduleManager

app = Flask(__name__)

# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyMealScheduleManager:
    def set_one_meal_schedule(self, account_id: int, target_date: str, meal_type: str, required: bool, return_time: str, message: str):
        """元のMealScheduleManagerの登録ロジックを再現"""
        print(f"[Manager] 予定を登録します。アカウントID: {account_id}")
        print(f"[Manager] 日付: {target_date}, 食事タイプ: {meal_type}")
        print(f"[Manager] 食事必要フラグ: {required}")
        print(f"[Manager] 帰宅時間: '{return_time}', メッセージ: '{message}'")
        print(f"[Manager] 保存が完了しました。")

# マネージャーのインスタンス化
meal_schedule_manager = DummyMealScheduleManager()


# ==========================================
# 境界層（HTML/JavaScript テンプレート定義）
# ==========================================
# Tkinterの toggle_input_fields() の動きを、JavaScript（showHideFields）で完全再現しています
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>予定入力</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 22px; color: #333; margin-bottom: 20px; }
        .radio-group { margin: 20px 0; font-size: 18px; }
        .radio-group label { margin: 0 15px; cursor: pointer; }
        .input-field { text-align: left; margin: 15px 0; }
        .input-field label { font-weight: bold; font-size: 14px; }
        input[type="text"] { width: 95%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        input[type="submit"] { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; font-weight: bold; margin-top: 15px; }
        input[type="submit"]:hover { background-color: #0056b3; }
    </style>
    <script>
        // Tkinterの toggle_input_fields に相当するJavaScript処理
        function showHideFields() {
            var isRequired = document.getElementById('required_true').checked;
            var detailFrame = document.getElementById('detail_frame');
            if (isRequired) {
                detailFrame.style.display = 'block';
            } else {
                detailFrame.style.display = 'none';
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>{{ target_date }} の {{ meal_name }}</h2>
        
        <form action="/meal-input" method="POST">
            <input type="hidden" name="target_date" value="{{ target_date }}">
            <input type="hidden" name="meal_type" value="{{ meal_type }}">

            <div class="radio-group">
                <label>
                    <input type="radio" id="required_true" name="required" value="true" checked onclick="showHideFields()"> 必要
                </label>
                <label>
                    <input type="radio" id="required_false" name="required" value="false" onclick="showHideFields()"> 不要
                </label>
            </div>
            
            <div id="detail_frame">
                <div class="input-field">
                    <label>帰宅時間</label>
                    <input type="text" name="return_time" placeholder="例: 19:00">
                </div>
                <div class="input-field">
                    <label>メッセージ</label>
                    <input type="text" name="message" placeholder="例: ごはんいります">
                </div>
            </div>
            
            <input type="submit" value="登録">
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（表示と登録処理）
# ==========================================
@app.route('/meal-input', methods=['GET', 'POST'])
def meal_input_view():
    # 本来はカレンダー画面から渡される想定の変数（単体テスト用にデフォルト値を設定）
    target_date = request.args.get('date', '2026-07-10')
    meal_type = request.args.get('type', 'lunch')  # breakfast / lunch / dinner

    # 元のコードにあった食事名マッピング辞書
    meal_name_dict = {
        "breakfast": "朝食",
        "lunch": "昼食",
        "dinner": "夕食"
    }
    meal_name = meal_name_dict.get(meal_type, "食事")

    # --- 登録ボタンが押されたときの処理 (Tkinterの register_schedule に対応) ---
    if request.method == 'POST':
        # フォームからデータを取得
        form_date = request.form.get('target_date')
        form_type = request.form.get('meal_type')
        required_str = request.form.get('required')
        
        # 文字列の 'true' / 'false' を Python の Boolean に変換
        required = True if required_str == 'true' else False

        # 「必要」なら入力値を採用、「不要」なら空文字にする元のロジックを完全再現
        if required:
            return_time = request.form.get('return_time', '').strip()
            message = request.form.get('message', '').strip()
        else:
            return_time = ""
            message = ""

        # マネージャーのメソッドを呼び出して登録
        meal_schedule_manager.set_one_meal_schedule(
            account_id=1,  # 元コードの固定値
            target_date=form_date,
            meal_type=form_type,
            required=required,
            return_time=return_time,
            message=message
        )
        
        return redirect(url_for('success_page'))

    # --- 画面を初めて開いたときの処理 (Tkinterの display に対応) ---
    return render_template_string(
        HTML_TEMPLATE, 
        target_date=target_date, 
        meal_type=meal_type, 
        meal_name=meal_name
    )


@app.route('/success')
def success_page():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 登録完了</h1>
        <p>予定を登録しました。</p>
        <a href="/meal-input" style="font-size: 18px; color: #007bff;">戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)