#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask_mail import Mail, Message
from module import sort_newest, convert, address, to_text

#convert("./sound")
#test1 = to_text("./sound")
#print (test1)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'harayusuke.test@gmail.com'
app.config['MAIL_PASSWORD'] = 'hawelka1'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

@app.route("/")
def index():
    return '<p>音声を録音してください</p><form action="/to_speech" method="GET"><button type="submit">変換開始</button></form>'

test1 = "failed"
@app.route("/to_speech")
def to_speech():
    global test1
    test1 = to_text("./sound")
    return '<p>変換完了</p><form action="/choice" method="GET"><button type="submit">送信先選択</button></form>'

@app.route("/choice")
def choice():
    return render_template('send_list.html')

add = ""
@app.route("/edit")
def edit():
    user = request.args.get('user', '')
    global add
    add = address("{}".format(user))
    print (add)
    return '<form action="/send" method="GET"><textarea name="変換結果">{}</textarea><input type="submit" value="完了"></form>'.format(test1)

result = ""
@app.route("/send")
def send():
    global result
    result = request.args.get('変換結果', '')
    return '<form action="/last" method="GET"><textarea name="編集結果">{}</textarea><input type="submit" value="送信"></form>'.format(result)

@app.route("/last")
def last():
    msg = Message("from {名前}",
                  sender="harayusuke.test@gmail.com",
                  recipients=["{}".format(add)])
    msg.body = "{}".format(result)
    #msg.html = "<b>testing</b>"
    mail.send(msg)
    return "送信完了"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')