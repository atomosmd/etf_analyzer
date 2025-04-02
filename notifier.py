# notifier.py
import requests

ACCESS_TOKEN = "kydB7Xv2ZeeF7JGE7szMkGeBMXO9Iq6wAAAAAQoNFKMAAAGV9saWJsO6S6yUo1la"

def send_kakao_message(message: str):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {
        "template_object": str({
            "object_type": "text",
            "text": message,
            "link": {
                "web_url": "https://finance.naver.com",
                "mobile_web_url": "https://finance.naver.com"
            },
            "button_title": "확인"
        }).replace("'", '"')  # JSON 형식 맞추기
    }

    res = requests.post(url, headers=headers, data=data)
    print(f"[카카오톡] 전송 상태: {res.status_code}, 응답: {res.text}")
