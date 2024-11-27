import requests
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tests import Test
import random
url = "http://127.0.0.1:5000/test"

payload = {"text": "test_user"}

num_requests = 2
check_point_num = 1000
def send_request():
    try:
        print(requests.post("http://localhost:8000/test", json={"text" : f" Hello World! {datetime.now()}" }).status_code )
        
        # response = requests.post(url, json=payload)
        # print(f"Response: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")



def flood_test():

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
        num_requests = random.randint(1,30)
        for num in range(num_requests):

            executor.submit(send_request)
            if (num+1) % check_point_num == 0: 
                print(f"Attack in progress {num+1}")

if __name__ == "__main__":
    flood_test()
