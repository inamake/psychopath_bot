# -*- coding: utf-8 -*-

from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    QuickReplyButton, MessageAction, QuickReply, CarouselTemplate, CarouselColumn,
)
import os

app = Flask(__name__)


#環境変数取得

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

'''
#おうむ返しする。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add()
'''

'''
#クイックリプライ機能の実装（診断）
@handler.add(MessageEvent, message=TextMessage)
def diagnosis_question1(event):
    answer_list = [1, 2, 3, 4, 5]
    question = "診断①(選択肢1〜5で答えてください。)"

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}")) for language in answer_list]


    messages = TextSendMessage(text=question,
                               quick_reply=QuickReply(items=items))

    line_bot_api.reply_message(event.reply_token, messages=messages)
'''


#キャラセルカラム機能実装（診断）
@app.route("/")
@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    notes = [CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle02.jpg",
                            title="行動を先延ばしにする人",
                            text="決断出来ない、失敗を恐れる人、完璧主義者かを診断",
                            actions=[{"type": "uri","label": "診断","uri": "https://psychopathbot.herokuapp.com/putOffTest"}]),

              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle03.jpg",
                             title="テスト",
                             text="テスト",
                             actions=[
                                 {"type": "message", "label": "診断", "text": "#テスト"}]),

              CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle04.jpg",
                             title="テスト",
                             text="テスト",
                             actions=[
                                 {"type": "message", "label": "診断", "text": "#テスト"}])

             ]

    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=notes),
    )

    line_bot_api.reply_message(event.reply_token, messages=messages)


@app.route("/putOffTest")
def putOffTest():
    return render_template('putOffTest.html', title="実行あるのみ")

totalReply = None
@app.route("/result")
def result():
    replyList = []
    answerList = [0, 1, 2, 3]
    global totalReply
    total = request.args.get('total', '')
    for num in range(int(total)):
        testNumber = 'test{}'.format(num)
        reply = request.args.get('{}'.format(testNumber), '')
        result = int(reply)
        if result in answerList:
            replyList.append(result)

    if int(total) == len(replyList):
        totalReply = sum(replyList)
        return "{}".format(totalReply)
    else:
        return "全てに回答して下さい"
    # reply = request.args.get('test1', '')
    # return "{}".format(reply)

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)