import requests

print("Get workers")
response_workers = requests.get("http://localhost:5000/workers")
print(response_workers.json())

print("Get existing worker")
response_worker = requests.get("http://localhost:5000/workers/1010")
print(response_worker.json())

print("Get non-existent worker")
response_worker_non_existent = requests.get("http://localhost:5000/workers/1050")
print(response_worker_non_existent.json())

print("Post new worker")
query1 = {"worker_id": "1020", "name":"Joe Pass", "shifts": {"27-06-2022":"0-8"}}
post = requests.post("http://localhost:5000/workers", json=query1)
response1 = requests.get("http://localhost:5000/workers")
print(f'POST response status code: {response1.status_code}')
print(response1.json())

print("Put existing worker shifts")
query2 = {"shifts": {"27-06-2022":"0-8", '01-07-2022': '0-8'}}
put = requests.put("http://localhost:5000/workers/1012", json=query2)
response2 = requests.get("http://localhost:5000/workers")
print(f'PUT response status code: {response2.status_code}')
print(response2.json())

print("Delete existing worker")
delete = requests.delete("http://localhost:5000/workers/1020")
response3 = requests.get("http://localhost:5000/workers")
print(response3.json())