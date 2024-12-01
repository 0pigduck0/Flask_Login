from flask import Flask, render_template, request, redirect, session, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 파일 경로
USER_FILE = "users.txt"
MEMO_FILE = "memos.txt"

# 사용자 파일 확인 및 생성
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        pass

if not os.path.exists(MEMO_FILE):
    with open(MEMO_FILE, "w") as f:
        pass

@app.route("/")
def main():
    if 'username' in session:
        # 메인 페이지 - 사용자 이름과 메모 표시
        with open(MEMO_FILE, "r") as f:
            memos = [line.strip() for line in f.readlines()]
        return render_template("main.html", username=session['username'], memos=memos)
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        password = request.form["password"]
        # 사용자 파일 읽기
        with open(USER_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        for user in users:
            if user[1] == user_id and user[2] == password:
                session['username'] = user[0]
                flash(f"환영합니다, {user[0]}님!")
                return redirect(url_for("main"))
        flash("아이디 또는 비밀번호가 일치하지 않습니다.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        user_id = request.form["id"]
        password = request.form["password"]
        # 사용자 파일 읽기
        with open(USER_FILE, "r") as f:
            users = [line.strip().split(",") for line in f.readlines()]
        if any(user[1] == user_id for user in users):
            flash("이미 존재하는 아이디입니다.")
            return render_template("signup.html")
        # 새로운 사용자 추가
        with open(USER_FILE, "a") as f:
            f.write(f"{name},{user_id},{password}\n")
        flash("회원가입이 완료되었습니다. 로그인해주세요!")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("로그아웃되었습니다.")
    return redirect(url_for("main"))

@app.route("/memo", methods=["POST"])
def memo():
    if 'username' in session:
        content = request.form["content"]
        if content.strip():
            with open(MEMO_FILE, "a") as f:
                f.write(f"{session['username']}:{content}\n")
        flash("메모가 저장되었습니다.")
        return redirect(url_for("main"))
    flash("로그인이 필요합니다.")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
