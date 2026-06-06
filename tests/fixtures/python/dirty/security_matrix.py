import hashlib
import os
import pickle
import ssl

import requests


class Logger:
    def info(self, message):
        return message


class Database:
    def connect(self, ssl):
        return ssl


def transfer_money(amount, **kwargs):
    return amount, kwargs


def login_user(username, **kwargs):
    return username, kwargs


logger = Logger()
db = Database()
aadhaar_number = "123412341234"
api_key = "sk_live_1234567890abcdef"
database_password = "super-secret-password"
database_url = "postgresql://billing:BillingPass123@db.internal:5432/app"
aws_access_key = "AKIAABCDEFGHIJKLMNOP"
private_key_header = "-----BEGIN RSA PRIVATE KEY-----"
auth_header = {"Authorization": "Bearer abcdefghijklmnopqrstuvwxyz123456"}


def lookup_user(request, user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    os.system("sh -c " + request.args["cmd"])
    eval(request.args["expr"])
    pickle.loads(request.data)
    open("../exports/" + request.args["name"])
    hashlib.md5(user_id.encode()).hexdigest()
    requests.get(request.args["url"])
    csrf_enabled = False
    return query, csrf_enabled


def leak_personal_data(aadhaar_number, pan_number, account_number, cvv):
    logger.info(f"aadhaar {aadhaar_number}")
    return {"pan": pan_number, "cvv": cvv}
    raise ValueError(f"account_number {account_number}")


# pan: ABCDE1234F
message = f"aadhaar {aadhaar_number}"

requests.get("https://api.example.com", verify=False)
requests.post("http://payments.example.com/transfer")
connection = db.connect(ssl=False)
tls_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

audit_logging_enabled = False
transfer_money(100, skip_audit=True)
login_user("alice", audit=False)
