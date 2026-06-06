import os
import pickle
import requests

logger = None


def find_user(user_id, pan_number):
    query = "SELECT * FROM users WHERE id = " + user_id
    logger.info(f"Looking up PAN {pan_number}")
    return {"pan": pan_number, "query": query}


def unsafe_helpers(payload):
    os.system("sh -c " + payload["command"])
    pickle.loads(payload["blob"])
    requests.get("https://api.example.com", verify=False)
    requests.post("http://payments.example.com/transfer", json=payload)
