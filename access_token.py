import requests

REST_API_KEY = '31c61ad13b76c7ef2fa2ab5204a2f660'
REDIRECT_URI = 'http://localhost:8080'
AUTH_CODE = '04KfZzSDi_Vf78bM9NBWS46EKWwm74IJrz0IdtfziyBXy4E1oXMlJQAAAAQKFxDvAAABlfbEB7jSDh85zpcCzQ'

url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": REST_API_KEY,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE,
}

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)