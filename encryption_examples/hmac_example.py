from utils import Utils
import json


# HMAC (Hash-Based Message Authentication Code) is a cryptographic technique that combines a hash function with a secret key to 
# ensure message integrity and verify that the message has not been tampered with during transmission
data = {
    "user_id": 12345,
    "amount": 500,
    "timestamp": "2024-11-30T15:00:00"
}

key = "supersecretkey"

hmac_value = Utils.compute_hmac(data, key)

payload = {
    "data": data,
    "hmac": hmac_value
}

payload_json = json.dumps(payload)
print(f"Payload Sent: {payload_json}")

payload_received = json.loads(payload_json)

key = "supersecretkey"

if Utils.verify_hmac(payload_received, key):
    print("Congrats! Data is authentic and has not been tampered with.")
else:
    print("Warning!! Data verification failed. Possible tampering detected or wrong key.")