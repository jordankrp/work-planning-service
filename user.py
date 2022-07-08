import requests
import json
from blessed import Terminal
from PyInquirer import prompt

options_menu = ["Display all workers", "Display specific worker", "Add new worker", "Add/ edit shift", "Delete shift", "Delete worker"]

term = Terminal()

def print_start_screen():
    print(term.home + term.clear)

    print(term.center(term.bold(("Welcome to the work planning user interface"))))

    print("\n\n")

    input_prompt = prompt(
        {
            "name": "action",
            "type": "list",
            "message": "Choose an action to continue",
            "required": True,
            "choices": options_menu,
        }
    )
    print('\n')
    return input_prompt

def display_all_workers():
    workers = requests.get("http://localhost:5000/workers")
    for worker in workers.json():
    	print(f"Name: {worker['name']}")
    	print(f"Worker ID: {worker['worker_id']}")
    	for date in worker['shifts']:
    		print(f"{date}: {worker['shifts'][date]}")
    	print('\n')

def get_worker_id():
    print(term.underline("Please type in the worker ID"))
    print()
    answer = prompt(
            {
                "type": "input",
                "name": "worker_id",
                "message": "Worker ID:",
                #"validate": greengrass_group_validation,
            }
        )
    return str(answer)

def display_worker(worker_id):
	worker = requests.get(f"http://localhost:5000/worker/{worker_id}")
	print(json.loads(worker))
	#print(f"Name: {worker.json()['name']}")
	#print(f"Worker ID: {worker.json()['worker_id']}")
	#for date in worker.json()['shifts']:
	#	print(f"{date}: {worker.json()['shifts'][date]}")
	#print('\n')

if __name__ == "__main__":

    input_prompt = None
    while not input_prompt:
        input_prompt = print_start_screen()
    if input_prompt["action"] == options_menu[0]:
        display_all_workers()
    elif input_prompt["action"] == options_menu[1]:
        worker_id = get_worker_id()
        display_worker(worker_id)
    else:
    	print("All other options")