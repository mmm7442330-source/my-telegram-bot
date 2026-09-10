import json
import time
import urllib.request
import urllib.parse

TOKEN = "ضع_التوكن_هنا"
API = f"https://api.telegram.org/bot{TOKEN}/"

def request(method, data=None):
    if data:
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(API + method, data=data)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def send_message(chat_id, text):
    request("sendMessage", {
        "chat_id": chat_id,
        "text": text
    })

def delete_message(chat_id, message_id):
    request("deleteMessage", {
        "chat_id": chat_id,
        "message_id": message_id
    })

def ban_user(chat_id, user_id):
    request("banChatMember", {
        "chat_id": chat_id,
        "user_id": user_id
    })

def mute_user(chat_id, user_id):
    request("restrictChatMember", {
        "chat_id": chat_id,
        "user_id": user_id,
        "permissions": json.dumps({
            "can_send_messages": False
        })
    })

def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user = message.get("from", {})

    if text == "/start":
        send_message(chat_id, "هلا 👋 أنا بوت الإدارة الخاص بك.")

    elif text == "/help":
        send_message(
            chat_id,
            "أوامر الإدارة:\n"
            "/ban - حظر العضو بالرد على رسالته\n"
            "/mute - كتم العضو بالرد على رسالته\n"
            "/del - حذف الرسالة بالرد عليها\n"
            "/rules - عرض القوانين"
        )

    elif text == "/rules":
        send_message(chat_id, "📜 قوانين المجموعة:\n1- الاحترام\n2- ممنوع السبام\n3- ممنوع نشر الروابط بدون إذن")

    elif text == "/del":
        reply = message.get("reply_to_message")
        if reply:
            delete_message(chat_id, reply["message_id"])
            delete_message(chat_id, message["message_id"])

    elif text == "/ban":
        reply = message.get("reply_to_message")
        if reply:
            ban_user(chat_id, reply["from"]["id"])
            delete_message(chat_id, message["message_id"])

    elif text == "/mute":
        reply = message.get("reply_to_message")
        if reply:
            mute_user(chat_id, reply["from"]["id"])
            delete_message(chat_id, message["message_id"])

def main():
    offset = 0

    while True:
        try:
            result = request("getUpdates", {
                "offset": offset,
                "timeout": 30
            })

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
