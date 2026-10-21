import requests

url = 'https://www.musashino-u.ac.jp'

res = requests.get(url)

print(f"レスポンス:{res}")
print(f"レスポンスの型:{type(res)}")

print(f"リクエスト:{res.request}")
print(f"リクエストのヘッダー:{res.request.headers}")
print(f"リクエストのメソッド:{res.request.method}")
print(f"リクエストのurl:{res.request.url}")

print(f"ステータスコード:{res.status_code}")
print(f"ステータスメッセージ:{res.reason}")

print(f"レスポンスヘッダー:{res.headers}")