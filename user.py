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
                "message": "Worker ID:"
            }
        )
    return str(answer['worker_id'])

def display_worker(worker_id):
    req = requests.get(f"http://localhost:5000/workers/{worker_id}")
    if req.status_code == 200:
        worker = req.json()
        print(f"Name: {worker['name']}")
        print(f"Worker ID: {worker['worker_id']}")
        for date in worker['shifts']:
            print(f"{date}: {worker['shifts'][date]}")
        print('\n')
    else:
        print(req.text)
        
def get_new_worker_details():
    print(term.underline("Please type in the new worker ID"))
    print()
    answer = {}
    answer = prompt(
            {
                "type": "input",
                "name": "worker_id",
                "message": "Worker ID:"
            }
        )
    print()
    print(term.underline("Please type in the new worker name"))
    print()
    answer.update(
        prompt(
            {
                "type": "input",
                "name": "name",
                "message": "Worker name:"
            }
        )
    )
    print()
    print(term.underline("Please type in the number of shifts"))
    print()
    answer.update(
        prompt(
            {
                "type": "input",
                "name": "number_shifts",
                "message": "Number of shifts:"
            }
        )
    )

    number_shifts = int(answer['number_shifts'])

    shifts = {}
    for i in range(number_shifts):
        print(term.underline(f"Please type in the date of shift {i+1} in the format DD-MM-YYYY."))
        print()
        answer.update(
            prompt(
                {
                    "type": "input",
                    "name": f"shift_{i+1}_date",
                    "message": f"Shift {i+1} date:"
                }
            )
        )
        print()
        print(term.underline(f"Please type in the time of shift {i+1}. Accepted answers only 0-8, 8-16, 16-24."))
        print()
        answer.update(
            prompt(
                {
                    "type": "input",
                    "name": f"shift_{i+1}_time",
                    "message": f"Shift {i+1} time:"
                }
            )
        )
        print()
        shifts[answer[f"shift_{i+1}_date"]] = answer[f"shift_{i+1}_time"]

    return str(answer['worker_id']), str(answer['name']), dict(shifts)

def add_new_worker(worker_id, name, shifts):
    query = {"worker_id": str(worker_id), "name": str(name), "shifts": dict(shifts)}
    post = requests.post("http://localhost:5000/workers", json=query)
    if post.status_code == 201:
        print("New worker added successfully")
        display_worker(worker_id)
    else:
        print(post.text)

if __name__ == "__main__":

    input_prompt = None
    while not input_prompt:
        input_prompt = print_start_screen()
    if input_prompt["action"] == options_menu[0]:
        display_all_workers()
    elif input_prompt["action"] == options_menu[1]:
        worker_id = get_worker_id()
        display_worker(worker_id)
    elif input_prompt["action"] == options_menu[2]:
        worker_id, name, shifts = get_new_worker_details()
        add_new_worker(worker_id, name, shifts)
    else:
        print("All other options")