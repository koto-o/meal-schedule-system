from flask import Flask, render_template_string, request, redirect, url_for
# 本来は control.account_manager からインポートします
# from control.account_manager import AccountManager

app = Flask(__name__)

# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyAccountManager:
    def check_user_name_length(self, user_name: str) -> bool:
        """ユーザー名が1〜20文字であるかチェック（元ロジックの再現）"""
        length = len(user_name)
        return 1 <= length <= 20

    def register_user(self, user_name: str):
        """アカウントの登録処理"""
        print(f"[Manager] ユーザー名 '{user_name}' をシステムに登録しました。")

# マネージャーのインスタンス化
account_manager = DummyAccountManager()


# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 350px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 22px; margin-bottom: 20px; color: #333; }
        .input-field { text-align: left; margin: 15px 0; }
        .input-field label { font-weight: bold; font-size: 14px; }
        input[type="text"] { width: 93%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        .error-msg { color: #f44336; font-weight: bold; font-size: 14px; margin-bottom: 15px; text-align: left; }
        input[type="submit"] { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        input[type="submit"]:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>ユーザー登録</h2>
        
        {% if error_msg %}
            <div class="error-msg">⚠️ {{ error_msg }}</div>
        {% endif %}
        
        <form action="/account-registration" method="POST">
            <div class="input-field">
                <label>ユーザー名</label>
                <input type="text" name="user_name" value="{{ current_value }}" placeholder="例：お父さん">
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
@app.route('/account-registration', methods=['GET', 'POST'])
def account_registration_view():
    error_msg = None
    user_name = ""

    if request.method == 'POST':
        user_name = request.form.get('user_name', '').strip()
        
        if account_manager.check_user_name_length(user_name):
            account_manager.register_user(user_name)
            return redirect(url_for('success_page'))
        else:
            error_msg = "ユーザー名は1～20文字で入力してください"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=user_name)

    return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=user_name)


@app.route('/success')
def success_page():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 登録完了</h1>
        <p>ユーザーを登録しました。</p>
        <a href="/account-registration" style="font-size: 18px; color: #007bff;">戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)