import tkinter as tk
from tkinter import messagebox
import re


# シーケンス図の :MealScheduleManager（コントロール層）を模したクラス
class DummyMealScheduleManager:

    def set_return_time(
        self, user_id: str, target_date: str, time_slot: str, return_time: str
    ) -> None:
        """
        帰宅時間を確定し、UserCalenderに登録、GroupCalenderへ同期する
        (シーケンス図の confirm(..., returnTime) および syncSchedule() の流れに対応)
        """
        print(f"[Manager] 帰宅時間を登録します。対象日: {target_date} ({time_slot})")
        print(f"[Manager] 帰宅予定時間: {return_time}")
        print(f"[Manager] :UserCalender への登録が完了しました。")
        print(f"[Manager] :GroupCalender への syncSchedule() を実行しました。")


# シーケンス図の :ReturnTimePage（境界層）を表すクラス
class ReturnTimeInputView:

    def __init__(self, root: tk.Tk, schedule_manager: DummyMealScheduleManager):
        self.root = root
        self.schedule_manager = schedule_manager

        # 前の画面（MealRequirementPageなど）から引き継いだ想定のデータ
        self.current_user_id = "test_user_01"
        self.selected_date = "2026-06-26"
        self.selected_time_slot = "dinner"  # 朝食/昼食/夕食

        # ウィンドウの設定
        self.root.title("帰宅時間入力")
        self.root.geometry("400x220")

        self.create_widgets()

    def create_widgets(self):
        """
        システムが、帰宅予定時間の入力画面を表示する処理（シーケンス図の display() に対応）
        """
        # 案内ラベル
        self.label_hint = tk.Label(
            self.root,
            text="帰宅予定時間を入力してください\n(例: 19:30, 21:00)",
            font=("Arial", 11),
        )
        self.label_hint.pack(pady=15)

        # 時間入力欄（シーケンス図の submit(returnTime) で送られる要素）
        self.entry_return_time = tk.Entry(self.root, font=("Arial", 12), width=20)
        self.entry_return_time.pack(pady=10)
        self.entry_return_time.insert(0, "19:00")  # デフォルト値

        # ボタン配置用のフレーム
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=15)

        # 登録ボタン（シーケンス図の submit(returnTime) をトリガーするボタン）
        self.btn_submit = tk.Button(
            self.btn_frame,
            text="登録する",
            command=self.click_submit,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            width=10,
        )
        self.btn_submit.pack(side=tk.LEFT, padx=10)

        # キャンセルボタン
        self.btn_cancel = tk.Button(
            self.btn_frame,
            text="キャンセル",
            command=self.root.destroy,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            width=10,
        )
        self.btn_cancel.pack(side=tk.LEFT, padx=10)

    def click_submit(self):
        """
        ユーザーが帰宅時間を送信（確定）したときのイベントハンドラ
        """
        return_time = self.entry_return_time.get().strip()

        print(f"[View] 帰宅時間が入力されました。時間: {return_time}")

        # 簡易的な時間フォーマットバリデーション (HH:MM 形式チェック)
        if not re.match(r"^\d{1,2}:\d{2}$", return_time):
            messagebox.showwarning(
                "入力エラー",
                "時間の形式が正しくありません。「19:30」のように入力してください。",
            )
            return

        try:
            # 1. マネージャーに帰宅時間の登録と同期を依頼
            # (シーケンス図の confirm(targetTime, mealRequirement, returnTime) から後ろの流れに対応)
            self.schedule_manager.set_return_time(
                self.current_user_id,
                self.selected_date,
                self.selected_time_slot,
                return_time,
            )

            # 成功メッセージを表示して画面を閉じる
            messagebox.showinfo("登録完了", "帰宅予定時間を登録・同期しました。")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("エラー", f"登録に失敗しました: {e}")


# アプリケーションの起動（単体テスト用）
if __name__ == "__main__":
    manager = DummyMealScheduleManager()
    root = tk.Tk()
    app = ReturnTimeInputView(root, manager)
    root.mainloop()
    import re
from datetime import date
from flask import Flask, redirect, render_template_string, request, url_for

# [モック用設定] テスト用にFlaskアプリをここで立ち上げられるようにしています
app = Flask(__name__)


# ==========================================
# コントロール層（DummyManger）
# ==========================================
class DummyMealScheduleManager:

    def set_return_time(
        self, user_id: str, target_date: str, time_slot: str, return_time: str
    ) -> None:
        """帰宅時間を確定し、UserCalendarに登録、GroupCalendarへ同期する

        (シーケンス図の confirm(..., returnTime) および syncSchedule()
        の流れに対応)
        """
        print(
            f"[Manager] 帰宅時間を登録します。対象日: {target_date} ({time_slot})"
        )
        print(f"[Manager] 帰宅予定時間: {return_time}")
        print(f"[Manager] :UserCalendar への登録が完了しました。")
        print(f"[Manager] :GroupCalendar への syncSchedule() を実行しました。")


# マネージャーのインスタンス化
schedule_manager = DummyMealScheduleManager()

# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
# Tkinterの create_widgets() や display() に対応する、スマホ向けの画面デザインです
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>帰宅時間入力</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .hint { font-size: 16px; margin-bottom: 15px; color: #555; }
        .error-msg { color: #f44336; font-weight: bold; margin-bottom: 15px; }
        input[type="text"] { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 18px; text-align: center; }
        .btn-group { display: flex; justify-content: space-around; margin-top: 20px; }
        .btn { width: 45%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; color: white; }
        .btn-submit { background-color: #4CAF50; }
        .btn-cancel { background-color: #f44336; line-height: 24px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>帰宅時間入力</h2>
        <p class="hint">帰宅予定時間を入力してください<br>(例: 19:30, 21:00)</p>
        
        {% if error_msg %}
            <p class="error-msg">{{ error_msg }}</p>
        {% endif %}
        
        <form action="/return-time" method="POST">
            <input type="text" name="return_time" value="{{ current_value }}" placeholder="19:00">
            
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
# ルーティング（コントローラー・ビューの仲介）
# ==========================================
@app.route("/return-time", methods=["GET", "POST"])
def return_time_view():
    # 前の画面から引き継いだ想定の固定データ（Tkinterの__init__内データに対応）
    current_user_id = "test_user_01"
    selected_date = "2026-06-26"
    selected_time_slot = "dinner"

    error_msg = None
    default_time = "19:00"

    # --- ユーザーが「登録する」ボタンを押したときの処理 (POST) ---
    if request.method == "POST":
        return_time = request.form.get("return_time", "").strip()
        print(f"[View] 帰宅時間が入力されました。時間: {return_time}")

        # 簡易的な時間フォーマットバリデーション (HH:MM 形式チェック)
        if not re.match(r"^\d{1,2}:\d{2}$", return_time):
            error_msg = (
                "時間の形式が正しくありません。「19:30」のように入力してください。"
            )
            # エラーがある場合は、入力内容を保持したまま画面を再表示
            return render_template_string(
                HTML_TEMPLATE, error_msg=error_msg, current_value=return_time
            )

        try:
            # 1. マネージャーに帰宅時間の登録と同期を依頼 (confirm と syncSchedule に対応)
            schedule_manager.set_return_time(
                current_user_id,
                selected_date,
                selected_time_slot,
                return_time,
            )
            # 登録成功したら完了画面へリダイレクト
            return redirect(url_for("success_page"))

        except Exception as e:
            error_msg = f"登録に失敗しました: {e}"
            return render_template_string(
                HTML_TEMPLATE, error_msg=error_msg, current_value=return_time
            )

    # --- 初めて画面を開いたときの処理 (GET) ---
    # シーケンス図の display() に対応
    return render_template_string(
        HTML_TEMPLATE, error_msg=error_msg, current_value=default_time
    )


@app.route("/success")
def success_page():
    return """
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1>🎉 登録完了しました！</h1>
        <p>帰宅予定時間を登録・同期しました。</p>
        <a href="/return-time" style="font-size: 18px; color: #007bff;">戻る</a>
    </div>
    """


# ==========================================
# アプリケーションの起動（単体テスト用）
# ==========================================
if __name__ == "__main__":
    # host='0.0.0.0' にすることで、同じWi-Fi内のスマホからの接続を許可
    app.run(host="0.0.0.0", port=5000, debug=True)