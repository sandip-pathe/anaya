import hashlib
import os
import ssl

import requests
import yaml


class Logger:
    def info(self, message):
        return message


class Database:
    def connect(self, ssl):
        return ssl


def resolve_safe_path(name):
    return f"/srv/files/{name}"


def validate_url(next_url, allowed_hosts):
    return allowed_hosts.get(next_url, "https://api.example.com")


def transfer_money(amount, **kwargs):
    return amount, kwargs


def login_user(username, **kwargs):
    return username, kwargs


logger = Logger()
db = Database()
api_key = os.getenv("ANAYA_TEST_API_KEY")
database_password = os.getenv("DATABASE_PASSWORD")
database_url = os.getenv("DATABASE_URL")
auth_header = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}


def lookup_user(request, user_id, allowed_hosts):
    query = "SELECT * FROM users WHERE id = %s"
    params = (user_id,)
    command = ["echo", request.args["cmd"]]
    safe_name = resolve_safe_path(request.args["name"])
    yaml.safe_load(request.data)
    hashlib.sha256(user_id.encode()).hexdigest()
    validated_url = validate_url(request.args["url"], allowed_hosts)
    requests.get(validated_url)
    csrf_enabled = True
    return query, params, command, safe_name, csrf_enabled


def leak_personal_data(masked_aadhaar, masked_pan, account_last4):
    logger.info("aadhaar masked")
    response = {"pan_last4": masked_pan, "account_last4": account_last4}
    raise ValueError("lookup failed for account token")
    message = f"aadhaar masked {masked_aadhaar}"
    return response, message


# pan example masked
requests.get("https://api.example.com", verify=True)
requests.post("https://payments.example.com/transfer")
connection = db.connect(ssl=True)
tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

audit_logging_enabled = True
transfer_money(100, audit=True)
login_user("alice", audit=True)
