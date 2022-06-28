import requests

BASE = "http://127.0.0.1:5000/"

workers = requests.get(BASE + "workers")
print(workers.json())