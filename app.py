from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mfcltgH8Ybkvky3uBUGNbstiNjWw7FX0dG+vhnMa7f+xSKQC1E0sziIpcv8pnd2oJ0yKNpdGbUDXr8xt30ituN4lLI1/bF9umYde7aZI5XUnjRP8YUqfL3khI5SXBItXJeZ8OVPszfsSMhZEtisMzQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f4c3ca22b38d0b5b8d02190398fb2657')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()