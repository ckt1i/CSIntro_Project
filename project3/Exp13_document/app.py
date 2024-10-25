from flask import Flask, render_template, request, redirect, url_for, session, flash 
import sqlite3

app = Flask(__name__)

app.secret_key = 'S4gOebtOWcqOWKquWKm+eliOeltw==U2FpZCBubyBtb3JlIGN'


DATABASE = 'project3/Exp13_document/users.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def authenticate(username , password):
    conn = connect_db()
    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = authenticate(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('index')) # 登录成功后重定向到主页
        else:
            flash('用户不存在或密码错误')
            return render_template('login.html')
    else:
        return render_template('login.html')



dataset=["BIT网络安全课程真有趣","Web安全演示实验打卡","祝同学们都能取得好成绩!"]

def xss_fliter(value):
    return value.replace('<', '?').replace('>', '?').replace('/','?')

@app.route("/index", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = ""
    if request.method == "POST":
        if request.form.get("submit") == "提交新评论":
            comment = xss_fliter(request.form.get("newComment").strip())
            print(type(comment))
            if comment:
                dataset.append(comment)
    elif request.method == "GET":
        if request.args.get("submit") == "提交":
            query = request.args.get("content").strip()
            if query:
                sub_dataset = [x for x in dataset if query in x]
                return render_template("index.html", query=query, comments=sub_dataset)
    return render_template("index.html", query=query, comments=dataset)

def user_is_logged_in():
    return False

if __name__ == "__main__":
    app.run(debug=True)
