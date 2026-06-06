import requests


api_key = "sk_live_1234567890abcdef"  # anaya: ignore ANAYA-SEC-001
database_password = "super-secret-password"  # anaya: ignore
requests.get("https://api.example.com", verify=False)  # anaya: ignore ANAYA-TLS-001
