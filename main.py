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
    FollowEvent,CarouselTemplate, CarouselColumn,QuickReplyButton,MessageAction,QuickReply
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
    answer_list = ["診断","結果"]
    question = "「診断」か「結果を選択してください。」"

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}")) for language in answer_list]


    messages = TextSendMessage(text=question,
                               quick_reply=QuickReply(items=items))

    line_bot_api.reply_message(event.reply_token, messages=messages)
'''

#友達追加時、アクション
@handler.add(FollowEvent)
def on_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="友達追加ありがとうございます。\nまずは、「診断」と入力して、複数の診断から選択してください。"))


#キャラセルカラム機能実装（診断）
@app.route("/")
@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    if event.message.text == "診断":
        userID = event.source.user_id
        notes = [CarouselColumn(thumbnail_image_url="https://2.bp.blogspot.com/-MJHtCJ8P8hk/U1T3u2lAqpI/AAAAAAAAfWA/cAilQiPCLuM/s800/figure_sleeping.png",
                                title="あなたはどのくらい先延ばし屋か",
                                text="決断出来ない、失敗を恐れる人、完璧主義者かを診断",
                                actions=[
                                    {"type": "uri","label": "診断", "uri": "https://psychopathbot.herokuapp.com/putOffTest?abc={}".format(userID)}])
                #
                # CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle03.jpg",
                #                 title="テスト",
                #                 text="テスト",
                #                 actions=[
                #                     {"type": "message", "label": "---", "text": "---"}]),
                #
                # CarouselColumn(thumbnail_image_url="https://renttle.jp/static/img/renttle04.jpg",
                #                 title="テスト",
                #                 text="テスト",
                #                 actions=[
                #                     {"type": "message", "label": "---", "text": ""}])

                ]

        messages = TemplateSendMessage(
            alt_text='template',
            template=CarouselTemplate(columns=notes),
        )

        line_bot_api.reply_message(event.reply_token, messages=messages)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="『診断』と送ってください。"))



@app.route("/putOffTest")
def putOffTest():
    user = request.args.get('abc', '')
    return render_template('putOffTest.html', title="『行動を先延ばしにする人』診断", abc=user)

@app.route("/result")
def result():
    replyList = []
    total = request.args.get('total', '')
    user = request.args.get('abc', '')
    for num in range(int(total)):
        testNumber = 'test{}'.format(num)
        reply = request.args.get('{}'.format(testNumber), '')
        result = int(reply)
        replyList.append(result)

    if int(total) == len(replyList):
        totalReply = sum(replyList)
        estimate = diagnostics_result(totalReply)
        return render_template('result.html', title="診断結果", estimate=estimate)
    else:
        return "全てに回答して下さい"
    # reply = request.args.get('test1', '')
    # return "{}".format(reply)


# 結果表示
def diagnostics_result(totalReply):
    if totalReply >= 0 and totalReply <= 11:
        result = "筋金入りの先延ばし屋。先延ばしにすることであなたの生活の質は大幅にさがっている。" \
                 "改善しよう！いますぐ！"

    elif totalReply >= 12 and totalReply <= 17:
        result = "かなりの先延ばし屋。しかし既に、現状に疑問を抱いてはいる。対処は可能だ。"

    elif totalReply >= 18 and totalReply <= 22:
        result = "そこそこの先延ばし屋で、改善の余地あり。でもおそらく、あなたならこの悪習を断ち切れるはずだ。"

    elif totalReply >= 23 and totalReply <= 28:
        result = "ときどき横道にそれることもあるが、だいたいにおいて先延ばしをする心配はあまりない。"

    elif totalReply >= 29 and totalReply <= 33:
        result = "自制心のあるきちんとした人。先延ばしをする心配は全くない。"

    else:
        result = "-*-ERROR-*-"

    return result


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)