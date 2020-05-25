# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session,url_for,jsonify,Blueprint
#時間ごとに処理する
import time
import re

app = Flask(__name__)

app.secret_key = 'sunabakoza'

#正規表現
def word_re(word):
    re_hiragana = re.compile(r'^[あ-ん\u30A1-\u30F4ー]+$')
    return re_hiragana.fullmatch(word)

@app.route('/',methods=["GET", "POST"])
def top():
    if request.method == "GET":
        return render_template("index.html")
    else:
        #テーマ名を入力してDBに保存
        theme = request.form.get("theme")
        if theme == "":
            noTheme = "テーマが入力されていません"
            return render_template("index.html",noTheme = noTheme)
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        c.execute("insert into themes values(null,?)", (theme,) )
        #テーマIDをthemeに代入
        c.execute("select id from themes where theme = ?",(theme,))
        theme_id = c.fetchone()
        conn.commit()
        conn.close()
        # theme_id が NULL(PythonではNone)じゃなければログイン成功
        if theme_id is None:
            # theme_id が設定されていないとトップページに戻す
            return render_template("index.html")
        else:
            session['theme_id'] = theme_id[0]
            return redirect("/shiritori")
        

@app.route('/shiritori',methods=["GET","POST"])
def shiritori():
    if request.method == "GET":
        if 'theme_id' is None:
            # theme_id が設定されていないとトップページに戻す
            return render_template("index.html")
        else:
            return render_template("shiritori.html")
    else:
        #sessionからtheme_idを取得
        theme_id = session['theme_id']
        word = request.form.get('words')
        #正規表現で入力をひらがな限定
        if word_re(word):
            conn = sqlite3.connect('service.db')
            c = conn.cursor()
            #db shiritori に theme_idと単語をインサート
            c.execute("insert into shiritori values(?,?,null)", (theme_id,word,))
            conn.commit()
            conn.close()
            return jsonify({'word_output':word,'error':'テスト'})
        else:
            return jsonify({'error' : 'ひらがなかカタカナで入力してください'})


# @app.route('/remind',methods=["GET","POST"])
# def remind():
#     if request.method == "GET":
#         if 'theme_id' is None:
#             # theme_id が設定されていないとトップページに戻す
#             return render_template("index.html")
#         else:
#             return render_template("remind.html")
#     else:
#         theme_id = session['theme_id']
#         conn = sqlite3.connect('service.db')
#         c = conn.cursor()
#         #db shiritori に theme_idと単語をインサート
#         c.execute("select ", (theme_id,)
#         conn.commit()
#         conn.close()
#         return render_template("remind.html")



## おまじない
if __name__ == "__main__":
    app.run(debug=True)