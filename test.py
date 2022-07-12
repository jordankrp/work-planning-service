import requests
import unittest

class TestAPI(unittest.TestCase):

    BASE = 'http://127.0.0.1:5000/'
    WORKERS = BASE + 'workers'

    worker_1010 = {
        'worker_id': '1010', 
        'name': 'Miles Davis', 
        'shifts': {
            '29-06-2022': '0-8', 
            '30-06-2022': '16-24'
        }
    }

    new_worker = {
        'worker_id': '1020',
        'name': 'Joe Pass',
        'shifts': {
            '10-07-2022': '0-8',
            '12-07-2022': '16-24'
        }
    }

    update_shift = {
        'shifts': {
            '29-06-2022': '16-24'
        }
    }

    wrong_shift = {
        'shifts': {
            '29-06-2022': '5-9'
        }     
    }

    updated_worker_1012 = {
        "worker_id": "1012", 
        "name": "Dizzy Gillespie", 
        "shifts": {
            "29-06-2022": "16-24", 
            "01-07-2022": "8-16"
        }
    }

    worker_wrong_date = {
        "worker_id": "1018", 
        "name": "Oscar Peterson", 
        "shifts": {
            "2022-08-07": "16-24"
        }
    }

    def test_1_get_all_workers(self):
        resp = requests.get(self.WORKERS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)
        print('Test 1 completed')
    
    def test_2_get_worker_1010(self):
        resp = requests.get(self.WORKERS + '/1010')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.worker_1010)
        print('Test 2 completed')

    def test_3_post_worker(self):
        resp = requests.post(self.WORKERS, json = self.new_worker)
        self.assertEqual(resp.status_code, 201)
        print('Test 3 completed')

    def test_4_delete_worker(self):
        resp = requests.delete(self.WORKERS + '/1020')
        self.assertEqual(resp.status_code, 204)
        print('Test 4 completed')
    
    def test_5_update_worker(self):
        resp = requests.put(self.WORKERS + '/1012', json = self.update_shift)
        self.assertDictEqual(resp.json(), self.updated_worker_1012)
        print('Test 5 completed')
    
    def test_6_wrong_worker_id(self):
        resp = requests.get(self.WORKERS + '/1090')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), 'Worker ID does not exist')
        print('Test 6 completed')
    
    def test_7_update_wrong_shift_format(self):
        resp = requests.put(self.WORKERS + '/1012', json = self.wrong_shift)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), 'Wrong shift format, must be 0-8, 8-16 or 16-24')
        print('Test 7 completed')
    
    def test_8_post_wrong_date_format(self):
        resp = requests.post(self.WORKERS, json = self.worker_wrong_date)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), 'Wrong date format, must be in the form dd-mm-yyyy')
        print('Test 8 completed')



if __name__ == '__main__':
    tester = TestAPI()

    tester.test_1_get_all_workers()
    tester.test_2_get_worker_1010()
    tester.test_3_post_worker()
    tester.test_4_delete_worker()
    tester.test_5_update_worker()
    tester.test_6_wrong_worker_id()
    tester.test_7_update_wrong_shift_format()
    tester.test_8_post_wrong_date_format()
    