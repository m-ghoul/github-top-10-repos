import requests

base = "http://127.0.0.1:5500/"
# GET request
response = requests.get(base + "top10")
print(response.json())