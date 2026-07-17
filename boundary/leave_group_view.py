from flask import Flask, render_template_string, request, redirect, url_for
# 本来は control.group_manager や control.account_manager からインポートします
# from control.group_manager import GroupManager
# from control.account_manager import AccountManager

app = Flask(__name__)

# ==========================================
# テスト用のダミー（本来は既存のControl/Entityを使用）
# ==========================================
class DummyUser:
    def __init__(self, account_id):
        self.account_id = 1  # ダミーのアカウントID

class DummyGroupManager:
    def get_user_group_id(self, account_id: int):
        # テスト用（Noneを返すと「所属グループなし」のエラーをシミュレートできます）
        return "group_tsubofamily_123"

    def remove_member(self, group_id: str, account_id: int):
        """グループからメンバーを削除（退出）する処理"""
        print(f"[Manager] グループ '{group_id}' から アカウントID: {account_id} を退出させました。")

class DummyAccountManager:
    def get_current_user(self):
        return DummyUser(account_id=1)

# マネージャーのインスタンス化
group_manager = DummyGroupManager()
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
    <title>グループ退出</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 350px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 20px; margin-bottom: 25px; color: #333; }
        .error-msg { color: #f44336; font-weight: bold; font-size: 14px; margin-bottom: 20px; text-align: left; }
        .btn-group { display: flex; justify-content: space-around; flex-direction: column; gap: 12px; margin-top: 20px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; color: white; box-sizing: border-box; display: block; }
        .btn-leave { background-color: #d9534f; }
        .btn-leave:hover { background-color: #c9302c; }
        .btn-cancel { background-color: #6c757d; }
        .btn-cancel:hover { background-color: #545b62; }
    </style>
</head>
<body>
    <div class="container">
        <h2>グループから退出しますか？</h2>
        
        {% if error_msg %}
            <div class="error-msg">⚠️ {{ error_msg }}</div>
        {% endif %}
        
        <form action="/leave-group" method="POST">
            <div class="btn-group">
                <input type="submit" class="btn btn-leave" value="退出する">
                <a href="/menu-placeholder" class="btn btn-cancel">キャンセル</a>
            </div>
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（退出処理）
# ==========================================
@app.route('/leave-group', methods=['GET', 'POST'])
def leave_group_view():
    error_msg = None

    # --- 「退出する」ボタンが押されたときの処理 (Tkinterの leave_group に対応) ---
    if request.method == 'POST':
        user = account_manager.get_current_user()

        # 1. ユーザー情報の取得チェック
        if user is None:
            error_msg = "ユーザー情報が取得できません"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg)

        # 2. 所属グループIDの取得
        group_id = group_manager.get_user_group_id(user.account_id)

        # 3. 所属グループの存在チェック
        if group_id is None:
            error_msg = "所属しているグループがありません"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg)

        # 4. 退出処理を実行
        group_manager.remove_member(group_id, user.account_id)
        
        # 成功時は完了画面へ
        return redirect(url_for('success_page'))

    # --- 画面を初めて開いたときの処理 (Tkinterの display に対応) ---
    return render_template_string(HTML_TEMPLATE, error_msg=error_msg)


@app.route('/success')
def success_page():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 退出完了</h1>
        <p>グループから退出しました。</p>
        <a href="/leave-group" style="font-size: 16px; color: #007bff;">戻る</a>
    </div>
    """

@app.route('/menu-placeholder')
def menu_placeholder():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h2>🏠 メインメニュー（仮）</h2>
        <a href="/leave-group" style="font-size: 16px; color: #007bff;">グループ退出画面へ</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)