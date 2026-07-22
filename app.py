from flask import Flask, render_template, request, redirect, session
from control.account_manager import AccountManager
from control.meal_schedule_manager import MealScheduleManager
from control.group_manager import GroupManager
import calendar
from datetime import date, timedelta

account_manager = AccountManager()
group_manager = GroupManager()
meal_manager = MealScheduleManager()

app = Flask(__name__)
app.secret_key = "meal_schedule_secret"

app.permanent_session_lifetime = timedelta(days=365)

def get_login_user():

    account_id = session.get("account_id")

    if account_id is None:
        return None

    return account_manager.get_user_by_id(account_id)

@app.route("/")
def index():

    user = get_login_user()

    # 既に登録済みならそのままメインへ
    if user is not None:
        return redirect("/main")

    # 初回だけ登録画面へ
    return redirect("/register")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    user_name = request.form["user_name"]

    if not account_manager.check_user_name_length(user_name):
        return render_template(
            "register.html",
            error="ユーザー名は1～6文字で入力してください"
        )

    user = account_manager.register_user(user_name)

    session.permanent = True
    session["account_id"] = user.account_id

    return redirect("/main")

@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():

    account_id = request.form["account_id"]

    user = account_manager.get_user_by_id(account_id)

    if user is None:
        return render_template(
            "login.html",
            error="アカウントIDが存在しません"
        )

    session["account_id"] = user.account_id

    return redirect("/main")

@app.route("/main")
def main():

    user = get_login_user()

    if user is None:
        return redirect("/")

    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    selected_date = request.args.get("selected_date")

    if year is None or month is None:
        today = date.today()
        year = today.year
        month = today.month

    month_calendar = calendar.monthcalendar(year, month)

    prev_year = year
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year += 1

    has_group = False
    if user is not None:
        has_group = group_manager.has_group(user.account_id)

    return render_template(
        "main.html",
        has_group=has_group,
        year=year,
        month=month,
        month_calendar=month_calendar,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        selected_date=selected_date
    )


@app.route("/meal/<target_date>")
def meal(target_date):

    user = get_login_user()

    if user is None:
        return redirect("/login")

    # 自分の予定があるか確認
    schedule = meal_manager.get_schedule(
        user.account_id,
        target_date
    )

    group_id = group_manager.get_user_group_id(
        user.account_id
    )

    if group_id is None:

        schedules = meal_manager.get_user_schedule(
            user.account_id,
            target_date
        )

    else:

        schedules = meal_manager.get_group_schedule(
            group_id,
            target_date
        )

    return render_template(
        "meal.html",
        target_date=target_date,
        schedules=schedules,
        schedule=schedule,
        user=user
    )

@app.route("/meal_detail/<target_date>", methods=["GET", "POST"])
def meal_detail(target_date):

    user = get_login_user()

    if user is None:
        return redirect("/")

    if request.method == "POST":

        breakfast = request.form["breakfast"] == "1"
        lunch = request.form["lunch"] == "1"
        dinner = request.form["dinner"] == "1"

        return_time = request.form["return_time"]

        breakfast_message = request.form["breakfast_message"]
        lunch_message = request.form["lunch_message"]
        dinner_message = request.form["dinner_message"]

    if len(breakfast_message) > 30:
        schedule = meal_manager.get_schedule(user.account_id, target_date)
        return render_template(
            "meal_detail.html",
            target_date=target_date,
            schedule=schedule,
            error="朝食メッセージは30文字以内で入力してください"
        )

    if len(lunch_message) > 30:
        schedule = meal_manager.get_schedule(user.account_id, target_date)
        return render_template(
            "meal_detail.html",
            target_date=target_date,
            schedule=schedule,
            error="昼食メッセージは30文字以内で入力してください"
        )

    if len(dinner_message) > 30:
        schedule = meal_manager.get_schedule(user.account_id, target_date)
        return render_template(
            "meal_detail.html",
            target_date=target_date,
            schedule=schedule,
            error="夕食メッセージは30文字以内で入力してください"
        )

        # 不要なら内容を消す
        if not breakfast:
            breakfast_message = ""

        if not lunch:
            lunch_message = ""

        if not dinner:
            dinner_message = ""
            return_time = ""

        meal_manager.set_schedule(
            user.account_id,
            target_date,

            breakfast,
            breakfast_message,

            lunch,
            lunch_message,

            dinner,
            dinner_message,

            return_time
        )

        return redirect(f"/main?selected_date={target_date}")

    schedule = meal_manager.get_schedule(
        user.account_id,
        target_date
    )

    return render_template(
        "meal_detail.html",
        target_date=target_date,
        schedule=schedule
    )

@app.route("/account")
def account():

    user = get_login_user()

    return render_template(
        "account.html",
        user=user
    )

@app.route("/delete_account", methods=["POST"])
def delete_account():

    user = get_login_user()

    account_manager.delete_user(user.account_id)

    return redirect("/")

@app.route("/group_create")
def group_create():
    return render_template("group_create.html")

@app.route("/group_create", methods=["POST"])
def group_create_post():

    user = get_login_user()
    group_name = request.form["group_name"]

    try:
        group_manager.create_group(
            user.account_id,
            group_name
        )
    except ValueError as e:
        return render_template(
            "group_create.html",
            error=str(e)
        )

    return redirect("/main")

@app.route("/add_member")
def add_member():
    return render_template("add_member.html")

@app.route("/add_member", methods=["POST"])
def add_member_post():

    user = get_login_user()

    group_id = group_manager.get_user_group_id(
        user.account_id
    )

    account_id = request.form["account_id"]

    try:
        group_manager.add_member(
            group_id,
            account_id
        )
    except ValueError as e:
        return render_template(
            "add_member.html",
            error=str(e)
        )

    return redirect("/main")

@app.route("/leave_group")
def leave_group():
    return render_template("leave_group.html")


@app.route("/leave_group", methods=["POST"])
def leave_group_post():

    user = get_login_user()

    group_id = group_manager.get_user_group_id(
        user.account_id
    )

    group_manager.remove_member(
        group_id,
        user.account_id
    )

    return redirect("/main")

def get_login_user():

    account_id = session.get("account_id")

    if account_id is None:
        return None

    return account_manager.get_user_by_id(account_id)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
