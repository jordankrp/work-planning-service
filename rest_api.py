from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Endpoints
# workers/{worker_id}/shifts/

# curl commands for testing
# curl -X GET http://localhost:5000/workers
# curl -X DELETE http://localhost:5000/workers/1015
# curl -X POST -H "Content-Type: application/json" -d '{"worker_id": "1020", "name":"Joe Pass", "shifts": {"27-06-2022":"0-8"}}' http://localhost:5000/workers
# curl -X PUT -H "Content-Type: application/json" -d '{"shifts": {"27-06-2022":"16-24"}}' http://localhost:5000/workers/1012

workers = [
    {
        "worker_id": "1010", 
        "name": "Miles Davis", 
        "shifts": {
            "29-06-2022": "0-8", 
            "30-06-2022": "16-24"
        }
    },
    {
        "worker_id": "1012", 
        "name": "Dizzy Gillespie", 
        "shifts": {
            "29-06-2022": "8-16", 
            "01-07-2022": "8-16"
        }
    }
]


parser = reqparse.RequestParser()

class WorkersList(Resource):
    def get(self):
         return workers

    def post(self):
        parser.add_argument('worker_id', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('shifts', type=dict)
        args = parser.parse_args()
        if args['name'] == None or args['worker_id'] == None or args['shifts'] == None:
            return "Please provide a worker ID, name and shifts."
        else:
            new_worker = {
                'worker_id': args['worker_id'],
                'name': args['name'],
                'shifts': args['shifts'],
            }
            workers.append(new_worker)
            return request.get_json(), 201

class Worker(Resource):
    def get(self, worker_id):
        for worker in workers:
            if worker['worker_id'] == worker_id:
                return worker
        return 'Worker ID does not exist', 404

    def put(self, worker_id):
        parser.add_argument('shifts', type=dict)
        args = parser.parse_args()
        for worker in workers:
            if worker['worker_id'] == worker_id:
                # Need to restrict shift values to 0-8, 8-16, 16-24
                # For existin date, shift will be overwritten
                if args['shifts'] in ['0-8', '8-16', '16-24']:
                    worker['shifts'] = {**worker['shifts'], **args['shifts']}
                else:
                    print("Please enter a valid shift: 0-8, 8-16, 16-24")
                return worker, 200
        return 'Worker ID does not exist', 404

    def delete(self, worker_id):
        for worker in workers:
            if worker['worker_id'] == worker_id:
                workers.remove(worker)
                return '', 204
        return "Not found", 404

api.add_resource(WorkersList, '/workers')
api.add_resource(Worker, '/workers/<worker_id>')

if __name__ == '__main__':
    app.run(debug=True)