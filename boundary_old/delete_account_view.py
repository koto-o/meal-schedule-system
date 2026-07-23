from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)


# ==========================================
# コントロール層（DummyManager）
# ==========================================
class DummyAccountManager:

    def delete_account(self, user_id: str) -> None:
        """アカウント情報をシステム、グループ、カレンダーから完全に削除する

        (シーケンス図の deleteAccount() から後ろの一連の流れに対応)
        """
        print(f"[Manager] ユーザーID: {user_id} の削除処理を開始します。")
        print(f"[Manager] :User エンティティから delete(accountID) を実行。")
        print(f"[Manager] :UserCalendar から delete() を実行。")
        print(
            f"[Manager] :GroupManager へ通知し、:Group からメンバー削除を実行。"
        )
        print(f"[Manager] :GroupCalendar から delete() を実行。")
        print(f"[Manager] アカウントの完全削除が完了しました。")


# マネージャーのインスタンス化
account_manager = DummyAccountManager()

# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
# Tkinterの警告色（#f44336）を踏襲し、スマホで見やすい警告画面にデザインしています
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>アカウント削除</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .warning-text { color: #f44336; font-size: 15px; font-weight: bold; line-height: 1.6; margin-bottom: 25px; }
        .btn-group { display: flex; justify-content: space-around; margin-top: 10px; }
        .btn { width: 45%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; color: white; text-align: center; }
        .btn-delete { background-color: #f44336; }
        .btn-cancel { background-color: #9E9E9E; line-height: 24px; }
    </style>
    <script>
        // Tkinterの messagebox.askyesno() に対応するJavaScriptの二重確認
        function confirmDeletion() {
            return confirm("最終確認\\n本当にアカウントを削除しますか？この操作は取り消せません。");
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>アカウント削除</h2>
        
        <p class="warning-text">
            アカウントを削除すると、これまでの食事予定や<br>
            所属しているグループのデータがすべて削除されます。<br>
            本当に削除しますか？
        </p>
        
        <form action="/delete-account" method="POST" onsubmit="return confirmDeletion();">
            <div class="btn-group">
                <input type="submit" class="btn btn-delete" value="削除する">
                <a href="/menu-placeholder" class="btn btn-cancel">削除しない</a>
            </div>
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（コントロール層との仲介）
# ==========================================
@app.route("/delete-account", methods=["GET", "POST"])
def delete_account_view():
    # 疑似ログインユーザーID
    current_user_id = "test_user_01"

    # --- ユーザーが「削除する」を選択し、二重チェックも通ったときの処理 (POST) ---
    if request.method == "POST":
        print("[View] 「削除する」が選択されました。")

        try:
            # 1. AccountManagerにアカウント削除を依頼（deleteAccount()）
            account_manager.delete_account(current_user_id)

            # 2. 削除後はサインアップ画面（SignUp Page）を模した完了画面へリダイレクト
            return redirect(url_for("signup_placeholder"))

        except Exception as e:
            return f"""
            <div style="text-align: center; margin-top: 50px; font-family: sans-serif; color: #f44336;">
                <h2>⚠️ エラーが発生しました</h2>
                <p>アカウントの削除に失敗しました: {e}</p>
                <a href="/delete-account">戻る</a>
            </div>
            """

    # --- 初めて確認画面を開いたときの処理（シーケンス図の display() ） (GET) ---
    return render_template_string(HTML_TEMPLATE)


# 遷移先の各プレースホルダー（テスト用）
@app.route("/signup-placeholder")
def signup_placeholder():
    print(
        "[View] ログイン画面/サインアップ画面（SignUp Page）へ遷移しました。"
    )
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>👋 アカウントの削除完了</h1>
        <p>アカウントは正常に削除されました。ご利用ありがとうございました。</p>
        <p style="color: #6c757d; font-size: 14px;">（ここから新しくアカウント登録画面等に繋がります）</p>
        <a href="/delete-account" style="color: #007bff;">テストをやり直す</a>
    </div>
    """


@app.route("/menu-placeholder")
def menu_placeholder():
    print(
        "[View] 「削除しない」が選択されました。メインメニュー画面に戻ります。"
    )
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h2>🏠 メインメニュー（仮）に戻りました</h2>
        <a href="/delete-account" style="font-size: 18px; color: #f44336;">もう一度アカウント削除画面へ</a>
    </div>
    """


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)