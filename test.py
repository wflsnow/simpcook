import requests
proxies = {"https": "http://127.0.0.1:7890"}
r = requests.get("https://www.google.com", proxies=proxies)
print(r.status_code)