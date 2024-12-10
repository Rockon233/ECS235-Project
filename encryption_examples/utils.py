import hmac
import hashlib
import json


class Utils:
    def compute_hmac(data, key):
        message = json.dumps(data).encode('utf-8')
        secret_key = key.encode('utf-8')
        
        hmac_object = hmac.new(secret_key, message, hashlib.sha256)
        return hmac_object.hexdigest()
    @staticmethod
    def verify_hmac(payload, key):
        data = payload["data"]
        received_hmac = payload["hmac"]

        recomputed_hmac = Utils.compute_hmac(data, key)

        return hmac.compare_digest(received_hmac, recomputed_hmac)