from flask import Flask, render_template, request, redirect, url_for
import pymysql 

app = Flask(__name__)

def getConnection():
  conn = pymysql.connect(host = "localhost", user = "root", password = "rlagmlcks12@", db = "mydb", charset="utf8")
  return conn

def insert_board(data):
  conn = getConnection()
  curs = conn.cursor()

  sql = "select max(idx) from board_tb"
  curs.execute(sql)
  row = curs.fetchone()

  if row[0] is None:
    idx = 1
  else:
    idx = row[0] + 1
  
  sql = 'select now()'
  curs.execute(sql)
  row = curs.fetchone()
  time = row[0]

  sql = "insert into board_tb (idx, title, content, id, date) values (%s, %s, %s, %s, %s)"
  curs.execute(sql, (idx, data['title'], data['content'], data['writer'], time))
  conn.commit()
  
  conn.close()

def getBoardlist(num):
  max_idx = num * 3
  min_idx = max_idx - 2

  conn = getConnection()
  curs = conn.cursor()
  
  sql = "select idx, title, id, date from board_tb where idx >= (%s) and idx <= (%s)"
  curs.execute(sql, (min_idx, max_idx ))
  rows = curs.fetchall()
  if rows is None:
    rows = []
  
  return rows

def getContentFromIdx(idx):

  conn = getConnection()
  curs = conn.cursor()

  sql = "select idx, content from board_tb where idx = (%s)"
  curs.execute(sql, idx)
  content = curs.fetchone()
  if content is None:
    return "내용이 없습니다."
  
  return content

def deleteContent(idx):

  conn = getConnection()
  curs = conn.cursor()

  sql = "delete from board_tb where idx = (%s)"
  curs.execute(sql, idx)
  conn.commit()
  conn.close()

@app.route('/')
def index():
  board_list = getBoardlist(1)
  return render_template("home.html", board_list = board_list)

@app.route('/write', methods=['GET', 'POST'])
def write():
  if request.method == "GET":
    return render_template('write.html')
  else:
    data = request.form
    insert_board(data)
    return redirect(url_for("index"))


@app.route('/board/<int:num>')
def board(num):
  board_list = getBoardlist(num)
  return render_template('home.html', board_list= board_list)



@app.route('/content/<int:idx>', methods=['GET', 'POST'])
def web(idx):
  if request.method == "GET":
    content = getContentFromIdx(idx)
    return render_template('content.html', content=content)
  else:
    data = request.form
    content = deleteContent(data['num'])
    return redirect(url_for('index'))
  
@app.route('/delete/<int:idx>')
def remove(idx):
  content = deleteContent(idx)
  return render_template('home.html',)


if __name__ == "__main__":
  app.run(port = 5000);
