import requests


api_key = "anaya_test_secret_1234567890"  # anaya: ignore ANAYA-SEC-001
database_password = "super-secret-password"  # anaya: ignore
requests.get("https://api.example.com", verify=False)  # anaya: ignore ANAYA-TLS-001
