from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyMealScheduleManager:

    def check_length(self, message: str) -> bool:
        """メッセージの文字数制限をチェックする (30文字以内)"""
        if len(message) > 30:
            return False
        return True

    def set_message(
        self, user_id: str, target_date: str, time_slot: str, message: str
    ) -> None:
        """メッセージをカレンダーに登録し、グループに同期する"""
        print(f"[Manager] メッセージを登録します。対象日: {target_date} ({time_slot})")
        print(f"[Manager] 内容: {message}")
        print(f"[Manager] :UserCalendar への set(message) が完了しました。")
        print(f"[Manager] :GroupCalendar への syncSchedule() を実行しました。")

# マネージャーのインスタンス化
schedule_manager = DummyMealScheduleManager()


# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>メッセージ入力</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .hint { font-size: 16px; margin-bottom: 15px; color: #555; }
        .error-msg { color: #f44336; font-weight: bold; margin-bottom: 15px; }
        input[type="text"] { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        .btn-group { display: flex; justify-content: space-around; margin-top: 20px; }
        .btn { width: 45%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; color: white; }
        .btn-submit { background-color: #4CAF50; }
        .btn-cancel { background-color: #f44336; line-height: 24px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>メッセージ入力</h2>
        <p class="hint">伝言・メッセージを入力してください<br>（30文字以内）</p>
        
        {% if error_msg %}
            <p class="error-msg">{{ error_msg }}</p>
        {% endif %}
        
        <form action="/message-input" method="POST">
            <input type="text" name="message" value="{{ current_value }}" placeholder="例：ごはんいります">
            
            <div class="btn-group">
                <input type="submit" class="btn btn-submit" value="登録する">
                <a href="/success" class="btn btn-cancel">キャンセル</a>
            </div>
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（コントロール層との仲介）
# ==========================================
@app.route('/message-input', methods=['GET', 'POST'])
def message_input_view():
    # 前の画面から引き継いだ想定の固定データ
    current_user_id = "test_user_01"
    selected_date = "2026-06-26"
    selected_time_slot = "dinner"
    
    error_msg = None
    
    # ユーザーが「登録する」ボタンを押したときの処理 (POST)
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        print(f"[View] メッセージが送信されました。内容: {message}")
        
        # 1. マネージャーに文字数チェックを依頼 (30文字チェック)
        is_valid = schedule_manager.check_length(message)
        
        if not is_valid:
            error_msg = "メッセージは30文字以内で入力してください。"
            # 入力された文字を保持したままエラー画面を再表示
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=message)
            
        try:
            # 2. マネージャーに登録と同期を依頼
            schedule_manager.set_message(
                current_user_id,
                selected_date,
                selected_time_slot,
                message
            )
            return redirect(url_for('success_page'))
            
        except Exception as e:
            error_msg = f"登録に失敗しました: {e}"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=message)

    # 画面を初めて開いたときの処理 (GET)
    return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value="")


@app.route('/success')
def success_page():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 登録完了しました！</h1>
        <p>メッセージを登録・同期しました。</p>
        <a href="/message-input" style="font-size: 18px; color: #007bff;">戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)