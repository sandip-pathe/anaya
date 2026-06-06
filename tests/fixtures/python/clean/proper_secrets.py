import os

api_key = os.getenv("API_KEY")
database_password = os.getenv("DATABASE_PASSWORD")
database_url = os.getenv("DATABASE_URL")
auth_header = {"Authorization": f"Bearer {os.getenv('SERVICE_TOKEN')}"}
