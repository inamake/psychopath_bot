# -*- coding: utf-8 -*-

from flask import Flask, request, abort

from collections import defaultdict

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage,
)
import os
import json

app = Flask(__name__)

#空の辞書を宣言
addressData = defaultdict(dict)

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

@handler.add(MessageEvent, message=LocationMessage)


#位置情報から住所、緯度、経度を返す。
#def return_address(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        [
#            TextSendMessage(text="住所:\n[{}]\n緯度:\n[{}]\n経度:\n[{}]".format(event.message.address,
#            event.message.latitude,event.message.longitude)),
#        ]
#    )

#位置情報からタイトル、郵便番号上3桁、郵便番号、住所、緯度、経度を辞書に入れて返す。
def address_info(event):
    global addressData
    title = event.message.title
    address = event.message.address
    latiude = event.message.latitude
    longitude = event.message.longitude
    postal_code_frist3 = address[4:7]
    addressData[postal_code_frist3]["tilte"] = title
    addressData[postal_code_frist3]["address"] = address
    addressData[postal_code_frist3]["latiude"] = latiude
    addressData[postal_code_frist3]["longitude"] = longitude

    #jsonファイル読み込み
    address_datas = open("address_data.json", 'r',)
    address_datas = json.load(address_datas)

    #アドレスの連結
    address_datas.update(addressData)

    #jsonファイル書き込み
    adddata = open("address_data.json", 'w')
    json.dump(address_datas, adddata)

    #postal_code = postal_code_frist3 + address[8:12]
    line_bot_api.reply_message(
        event.reply_token,
        [
            #TextSendMessage(text="郵便番号上3桁:\n[{}]\n住所:\n[{}]".format(Postal_code_frist3,Address)),
            TextSendMessage(text="{}".format(address_datas))
        ]
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
