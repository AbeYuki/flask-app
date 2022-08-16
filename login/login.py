from flask import Flask, request,render_template

app = Flask(__name__)

# login処理です
@app.route('/', methods=['GET', 'POST'])
def form():
    # ２回目以降データが送られてきた時の処理です
    if request.method == 'POST':
        print("POSTされたIDは？" + str(request.form['id']))
        print("POSTされたPASSWORDは？" + str(request.form['pwd']))
        return render_template('form.html')
    # １回目のデータが何も送られてこなかった時の処理です。
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port='5100',debug=True)