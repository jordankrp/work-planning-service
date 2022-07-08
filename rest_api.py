# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

workers = [
    {"worker_id": "1110", "name": "Miles Davis", "shifts": {"29-06-2022": "0-8", "30-06-2022": "16-24"}},
    {"worker_id": "1112", "name": "Dizzy Gillespie", "shifts": {"29-06-2022": "8-16", "31-06-2022": "0-8"}},
    {"worker_id": "1120", "name": "Charlie Parker", "shifts": {"30-06-2022": "0-8"}},
]

#def _find_next_id():
#    return max(worker["id"] for worker in workers) + 1

@app.get("/workers")
def get_workers():
    return jsonify(workers)

#@app.get("/workers/<int:worker_id>")
#def get_worker():
#    return jsonify(workers[worker_id])

@app.post("/workers")
def add_worker():
    if request.is_json:
        worker = request.get_json()
        #print(f"worker name is {worker["name"]}")
        #worker["id"] = _find_next_id()
        workers.append(worker)
        return worker, 201
    return {"error": "Request must be JSON"}, 415