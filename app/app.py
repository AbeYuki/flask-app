import sqlite3
from flask import Flask,render_template,request,g

app = Flask(__name__)

def get_db():
    # with app.app_context() について
    # 「g」はFlaskのインスタンスであるappのアプリケーションコンテキスト(app_context)に属するものとして動作することでエラーを回避
    # Flaskのルーティングするためのデコレータ（上記サンプルでは@app.route(‘/’)）にて、インスタンスを指定しているため、get_db内では明示的にアプリケーションコンテキストを指定していませんが、これを実行してもエラーにならない
    with app.app_context():
        if 'db' not in g:
            # データベースをオープンしてFlaskのグローバル変数に保存
            g.db = sqlite3.connect('TestDB.db')
        return g.db

@app.route('/')
def index():

    # データベースを開く
    con = get_db()

    # テーブル「商品一覧」の有無を確認
    cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='商品一覧'")

    for row in cur:
        if row[0] == 0:
            # テーブル「商品一覧」がなければ作成する
            cur.execute("CREATE TABLE 商品一覧(コード INTEGER PRIMARY KEY, 商品名 STRING, 値段 REAL)")
            # レコードを作る
            cur.execute(
                """INSERT INTO 商品一覧(コード, 商品名, 値段) 
                values(1, '苺のショートケーキ', 350),
                (2, 'チョコケーキ', 380),
                (3, 'パインケーキ', 380),
                (4, 'バニラアイス', 180),
                (5, 'チョコアイス', 200),
                (6, '紅茶アイス', 180),
                (7, 'りんごのアップルパイ', 250),
                (8, 'ホットコーヒー', 100),
                (9, 'コーラ', 120),
                (10, 'オレンジジュース', 120)
                """)
            con.commit()
    
    # 商品一覧を読み込み
    cur = con.execute("select * from 商品一覧 order by コード")
    data = cur.fetchall()
    con.close()

    return render_template('index.html', data = data)

@app.route('/result', methods=["POST"])
def result_post():
    # テンプレートから新規登録する商品名と値段を取得
    name = request.form["name"]
    price = request.form["price"]

    # データベースを開く
    con = get_db()

    # コードは既に登録されているコードの最大値＋１の値で新規登録を行う
    cur = con.execute("select MAX(コード) AS max_code from 商品一覧")
    for row in cur:
        new_code = row[0] + 1
    cur.close()

    # 登録処理
    sql = "INSERT INTO 商品一覧(コード, 商品名, 値段)values({},'{}',{})".format(new_code, name, price)
    con.execute(sql)
    con.commit()

    # 一覧再読み込み
    cur = con.execute("select * from 商品一覧 order by コード")
    data = cur.fetchall()
    con.close()

    return render_template('index.html', data = data)

#@app.route('/upate', methods=["POST"])
#def update_pos():
#    name = update.form["name"]
#    price = update.form["price"]
#    con = get_db()
#    try:
#    	con.execute("update 商品一覧 set 商品名=?,値段=? where 商品名=name",('name','price'))
#    
#    except sqlite3.Error as e:
#    	print("error",e.args[0])
#
#    con.commit()
#    con.close()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='5000',debug=True)
