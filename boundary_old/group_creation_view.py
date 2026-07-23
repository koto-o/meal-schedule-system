from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)


# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyGroupManager:

    def check_group_name_length(self, group_name: str) -> bool:
        """グループ名が1〜20文字であるかチェック（元ロジックの再現）"""
        length = len(group_name)
        return 1 <= length <= 20


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
    <title>グループ作成</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 350px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { font-size: 20px; margin-bottom: 20px; color: #333; }
        .input-field { text-align: left; margin: 15px 0; }
        input[type="text"] { width: 93%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        .error-msg { color: #f44336; font-weight: bold; font-size: 14px; margin-bottom: 15px; text-align: left; }
        input[type="submit"] { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; font-weight: bold; margin-top: 10px; }
        input[type="submit"]:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>グループ名を入力してください</h2>
        
        {% if error_msg %}
            <div class="error-msg">⚠️ {{ error_msg }}</div>
        {% endif %}
        
        <form action="/group-creation" method="POST">
            <div class="input-field">
                <input type="text" name="group_name" value="{{ current_value }}" placeholder="例：大坪家">
            </div>
            
            <input type="submit" value="作成">
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（入力と確認画面への遷移処理）
# ==========================================
@app.route("/group-creation", methods=["GET", "POST"])
def group_creation_view():
    error_msg = None
    group_name = ""

    # --- 「作成」ボタンが押されたときの処理 (Tkinterの create_group に対応) ---
    if request.method == "POST":
        group_name = request.form.get("group_name", "").strip()

        # マネージャーに文字数チェックを依頼
        if group_manager.check_group_name_length(group_name):
            # チェックOKなら、確認画面へグループ名をパラメータで渡してリダイレクト
            # 元のコードの GroupCreationConfirmationView(group_name).display() に対応する動きです
            return redirect(
                url_for("confirmation_placeholder", group_name=group_name)
            )
        else:
            # エラー時はメッセージをセットして自画面を再描画
            error_msg = "グループ名は1～20文字で入力してください"
            return render_template_string(
                HTML_TEMPLATE, error_msg=error_msg, current_value=group_name
            )

    # --- 画面を初めて開いたときの処理 (Tkinterの display に対応) ---
    return render_template_string(
        HTML_TEMPLATE, error_msg=error_msg, current_value=group_name
    )


# 前回の確認画面を簡易的にドッキングしてテストしやすくしています
@app.route("/group-creation-confirmation")
def confirmation_placeholder():
    name = request.args.get("group_name", "")
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h2>（ここは group_creation_confirmation_view のダミーです）</h2>
        <p>確認画面へ引き渡されたグループ名: <strong>{name}</strong></p>
        <a href="/group-creation">入力画面へ戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)