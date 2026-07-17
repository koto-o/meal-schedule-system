from flask import Flask, render_template_string
# 本来は control.account_manager からインポートします
# from control.account_manager import AccountManager

app = Flask(__name__)

# ==========================================
# テスト用のダミー（本来は既存のControl/Entityを使用）
# ==========================================
class DummyUser:
    def __init__(self, account_id, user_name):
        self.account_id = account_id
        self.user_name = user_name

class DummyAccountManager:
    def get_user(self):
        # テスト用データ（登録がない状態を試す時はここを None にしてください）
        return DummyUser(account_id="akari_m", user_name="明莉")

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
    <title>登録情報</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 350px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 22px; margin-bottom: 20px; color: #333; }
        .info-box { text-align: left; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #e9ecef; }
        .info-item { font-size: 16px; margin: 10px 0; }
        .no-data { color: #868e96; font-style: italic; }
        .btn-back { display: inline-block; width: 80%; padding: 10px; background-color: #6c757d; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>登録情報</h2>
        
        {% if user %}
            <div class="info-box">
                <div class="info-item"><strong>ユーザーID：</strong>{{ user.account_id }}</div>
                <div class="info-item"><strong>ユーザー名：</strong>{{ user.user_name }}</div>
            </div>
        {% else %}
            <p class="no-data">登録されていません</p>
        {% endif %}
        
        <a href="/menu" class="btn-back">戻る</a>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（表示処理）
# ==========================================
# シーケンス図や元の display() メソッドに対応するルート
@app.route('/registration-info')
def registration_info_view():
    # マネージャーからユーザー情報を取得
    user = account_manager.get_user()
    
    # HTMLテンプレートにユーザーデータを渡して画面を描画
    return render_template_string(HTML_TEMPLATE, user=user)

@app.route('/menu')
def menu_placeholder():
    return "<h3>ここはメインメニュー画面（仮）です</h3><a href='/registration-info'>登録情報を見る</a>"


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)