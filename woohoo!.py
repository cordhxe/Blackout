import subprocess
import time
import requests

WEBHOOK_URL = ""  

def is_charging():
    result = subprocess.run(["adb", "shell", "dumpsys", "battery"], capture_output=True, text=True)
    output = result.stdout
    return "AC powered: true" in output or "USB powered: true" in output

def send_alert():
    print("⚠️ ไฟหาย กำลังแจ้งไปที่ discord")
    
    data = {
        "content": "# โหลๆ ไฟบ้านดับไอ้ควาย",
        "username": "Power Monitor",
        "embeds": [
            {
                "title": "Power Status Alert",
                "description": "",
                "color": 16711680  
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"✅! Status code: {response.status_code}")
    except requests.exceptions.HTTPError as err:
        print(f"❌ Failed to send")

last_state = None

try:
    while True:
        charging = is_charging()
        if last_state is None:
            last_state = charging
        elif last_state and not charging:
            send_alert()
        last_state = charging
        time.sleep(0.1)
except KeyboardInterrupt:
    print("🛑")
