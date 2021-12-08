import sqlite3

from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = "song"     #암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')  #127.0.0.1:5000
def index():
    return render_template('index.html')
    #return "<h1>Welcome~ 방문을 환영합니다.</h1>"

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs1 = cur.fetchall()
    conn.close()
    return render_template('memberlist.html', rs=rs1)

@app.route('/memberview/<string:id>/')
def member_view(id):        #mid를 경로로 설정하고 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % (id)
    cur.execute(sql)
    rs = cur.fetchone()     #해당 1개의 자료를 반환받음
    conn.close()
    return render_template('member_view.html', rs=rs)


@app.route('/register/', methods = ['GET', 'POST'])    #url경로   ####반드시 대문자로 POST
def register():
    if request.method == 'POST':
            # 자료 수집
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member VALUES ('%s', '%s', '%s', '%s', '%s')"\
            % (id, pwd, name, age, date)
        cur.execute(sql)    #실행 함수
        conn.commit()   #커밋완료
        return redirect(url_for('memberlist'))      #url 결로로 이동
    else:
        return render_template('register.html')






@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        #자료를 전달받음
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' and passwd = '%s' " % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()  #DB에서 찾은 데이터 가져옴   (1개!!)
        conn.close()
        if rs:
            session['userID'] = id   # 세션 발급    #로그인하거나..뭐 그럴떄..?
            return redirect(url_for('index'))

        else:
            error = "아이디나 비밀번호가 일치하지 않습니다"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('userID')   #세션 삭제
    return redirect(url_for('index'))




app.run(debug=True)