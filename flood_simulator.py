import requests
import json
from concurrent.futures import ThreadPoolExecutor

url = "http://127.0.0.1:5000/test"

payload = {"name": "test_user", "age": 25, "email": "test@example.com"}

num_requests = 10000
check_point_num = 1000
def send_request():
    try:
        response = requests.post(url, json=payload)
        print(f"Response: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def flood_test():
    with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust workers as needed
        
        for num in range(num_requests):

            executor.submit(send_request)
            if (num+1) % check_point_num == 0: 
                print(f"Attack in progress {num+1}")

if __name__ == "__main__":
    flood_test()
