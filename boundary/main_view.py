import calendar
from datetime import date
from flask import Blueprint, abort, redirect, render_template, request, url_for

# 既存のマネージャー（コントロール層）をインポート
from control.account_manager import AccountManager
from control.group_manager import GroupManager

# FlaskのルーティングをまとめるBlueprint（設計図）を作成
main_view_blueprint = Blueprint("main_view", __name__)


class MainView:

    def __init__(self):
        self.account_manager = AccountManager()
        self.group_manager = GroupManager()

    def display(self):
        """元のTkinterの表示ロジックをFlaskのメインルーティングにマッピング"""

        # 1. ユーザーが登録されているかチェック
        if not self.account_manager.has_user():
            return render_template("index.html", mode="registration")

        # 2. カレンダーの年月を取得（クエリパラメータがなければ今月）
        try:
            year = int(request.args.get("year", date.today().year))
            month = int(request.args.get("month", date.today().month))
        except ValueError:
            year = date.today().year
            month = date.today().month

        # 前月・翌月の計算
        prev_year, prev_month = (
            (year - 1, 12) if month == 1 else (year, month - 1)
        )
        next_year, next_month = (
            (year + 1, 1) if month == 12 else (year, month + 1)
        )

        # 3. グループ情報の判定（メニューボタンの条件分岐用）
        user = self.account_manager.get_current_user()
        has_group = False
        if user is not None:
            has_group = self.group_manager.has_group(user.account_id)

        # 4. カレンダーマトリクスの生成
        month_calendar = calendar.monthcalendar(year, month)

        # 5. 選択された日付の詳細
        selected_date = request.args.get("date")

        return render_template(
            "index.html",
            mode="main",
            year=year,
            month=month,
            prev_year=prev_year,
            prev_month=prev_month,
            next_year=next_year,
            next_month=next_month,
            has_group=has_group,
            month_calendar=month_calendar,
            selected_date=selected_date,
        )

    def register_user_from_main(self):
        """ユーザー登録処理"""
        user_name = request.form.get("user_name", "").strip()

        if not self.account_manager.check_user_name_length(user_name):
            return "エラー: ユーザー名は1～20文字で入力してください", 400

        self.account_manager.register_user(user_name)

        # 登録完了後、トップページへリダイレクト
        return redirect(url_for("main_view.index_route"))


# --- Flaskがアクセスするためのルーティング定義 ---
main_view_instance = MainView()


@main_view_blueprint.route("/")
def index_route():
    return main_view_instance.display()


@main_view_blueprint.route("/register", methods=["POST"])
def register_route():
    return main_view_instance.register_user_from_main()


# その他のView（画面）への遷移定義
@main_view_blueprint.route("/registration-info")
def open_registration_info_view():
    from boundary.registration_info_view import RegistrationInfoView

    view = RegistrationInfoView()
    return view.display()


@main_view_blueprint.route("/group/create")
def open_group_creation_view():
    from boundary.group_creation_view import GroupCreationView

    view = GroupCreationView()
    return view.display()


@main_view_blueprint.route("/group/add-member")
def open_add_member_view():
    from boundary.add_member_view import AddMemberView

    view = AddMemberView()
    return view.display()


@main_view_blueprint.route("/group/leave")
def open_leave_group_view():
    from boundary.leave_group_view import LeaveGroupView

    view = LeaveGroupView()
    return view.display()