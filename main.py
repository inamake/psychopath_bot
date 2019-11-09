# -*- coding: utf-8 -*-

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply,
)
import os

app = Flask(__name__)

diagnosis_class_count = 0
diagnosis_question_count = 0

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

#おうむ返しする。
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))

#クイックリプライ機能の実装（診断）
@handler.add(MessageEvent, message=TextMessage)

def diagnosis_question_1(event):
    global diagnosis_class_count
    global diagnosis_question_count
    answer_list = [1, 2, 3, 4, 5]

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}")) for language in answer_list]

    if diagnosis_question_count == 0:
        messages = TextSendMessage(text="診断①(選択肢1〜5で答えてください。)",
                                   quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=messages)

        diagnosis_class_count = diagnosis_class_count + int(items)
        diagnosis_question_count += 1

    elif diagnosis_question_count == 1:
        messages = TextSendMessage(text="診断②(選択肢1〜5で答えてください。)",
                                    quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=messages)

        diagnosis_class_count = diagnosis_class_count + int(items)
        diagnosis_question_count += 1

    elif diagnosis_question_count == 2:
        messages = TextSendMessage(text="診断③(選択肢1〜5で答えてください。)",
                                   quick_reply=QuickReply(items=items))

        line_bot_api.reply_message(event.reply_token, messages=messages)

        diagnosis_class_count = diagnosis_class_count + int(items)
        diagnosis_question_count += 1

    elif diagnosis_question_count == 3:
        if diagnosis_class_count == 3:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="【診断結果】\nあなたはとても良いです。"))
            diagnosis_question_count = 0
        elif diagnosis_class_count > 3 and diagnosis_class_count <= 6:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="【診断結果】\nあなたは普通です。"))
            diagnosis_question_count = 0
        elif diagnosis_class_count > 6 and diagnosis_class_count <= 14:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="【診断結果】\nあなたはヤバイです。"))
            diagnosis_question_count = 0
        elif diagnosis_class_count == 15:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="【診断結果】\nあなたは超絶ヤバイです。"))
            diagnosis_question_count = 0

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
