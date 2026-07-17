from flask import Flask, render_template_string, request, redirect, url_for
# 本来は control.group_manager からインポートします
# from control.group_manager import GroupManager

app = Flask(__name__)

# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyGroupManager:
    def get_user_group_id(self, account_id: int):
        """テスト用に自分が所属するグループIDを返す（Noneを返すとエラーのテストができます）"""
        return "group_tsubofamily_123"

    def add_member(self, group_id: str, target_account_id: int):
        """グループにメンバーを追加する処理"""
        print(f"[Manager] グループ '{group_id}' に アカウントID: {target_account_id} を追加しました。")

# マネージャーのインスタンス化
group_manager = DummyGroupManager()


# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>メンバー追加</title>
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
        <h2>メンバー追加</h2>
        
        {% if error_msg %}
            <div class="error-msg">⚠️ {{ error_msg }}</div>
        {% endif %}
        
        <form action="/add-member" method="POST">
            <div class="input-field">
                <label>追加するアカウントID</label>
                <input type="text" name="account_id" value="{{ current_value }}" placeholder="例: 2">
            </div>
            
            <input type="submit" value="追加">
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（表示と追加処理）
# ==========================================
@app.route('/add-member', methods=['GET', 'POST'])
def add_member_view():
    current_account_id = 1  # 元コードの仮ログインユーザーIDを引き継ぎ
    error_msg = None
    account_id_str = ""

    # --- 「追加」ボタンが押されたときの処理 (Tkinterの add_member に対応) ---
    if request.method == 'POST':
        account_id_str = request.form.get('account_id', '').strip()
        
        # 1. 未入力チェック
        if not account_id_str:
            error_msg = "アカウントIDを入力してください"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=account_id_str)
            
        try:
            # 2. 数値変換チェック (元コードの ValueError ハンドリングを再現)
            target_account_id = int(account_id_str)
            
            # マネージャーから自分のグループIDを取得
            group_id = group_manager.get_user_group_id(current_account_id)
            
            # 3. 所属グループの存在チェック
            if group_id is None:
                error_msg = "自分が所属しているグループがありません"
                return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=account_id_str)
                
            # 4. メンバー追加処理の実行
            group_manager.add_member(group_id, target_account_id)
            
            # 登録成功時は完了画面へリダイレクト
            return redirect(url_for('success_page', added_id=target_account_id))
            
        except ValueError:
            error_msg = "アカウントIDは数字で入力してください"
            return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=account_id_str)

    # --- 画面を初めて開いたときの処理 (Tkinterの display に対応) ---
    return render_template_string(HTML_TEMPLATE, error_msg=error_msg, current_value=account_id_str)


@app.route('/success')
def success_page():
    added_id = request.args.get('added_id', '')
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 追加完了</h1>
        <p>アカウントID {added_id} を自分のグループに追加しました。</p>
        <a href="/add-member" style="font-size: 18px; color: #007bff;">戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)