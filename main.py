import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "online"

# جلب المتغيرات من بيئة العمل (Environment Variables)
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
usertoken = os.getenv("TOKEN")

SELF_MUTE = True
SELF_DEAF = False

# التحقق من وجود المتغيرات لمنع الأخطاء
if not usertoken:
    print("[ERROR] Please add a TOKEN inside your Environment Variables / Secrets.")
    sys.exit()

if not GUILD_ID:
    print("[ERROR] Please add a GUILD_ID inside your Environment Variables / Secrets.")
    sys.exit()

if not CHANNEL_ID:
    print("[ERROR] Please add a CHANNEL_ID inside your Environment Variables / Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

# دمج طلب التحقق وجلب البيانات في طلب واحد
validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = validate.json()
username = userinfo.get("username")
discriminator = userinfo.get("discriminator", "0")
userid = userinfo.get("id")

def joiner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    
    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }
    
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1,"d": None}))

def run_joiner():
    # تعديل بسيط ليعمل مسح الشاشة على نظامي الويندوز ولينكس
    os.system("clear" if os.name == "posix" else "cls")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)
        time.sleep(30)

keep_alive()
run_joiner()
