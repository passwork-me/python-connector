import os

from dotenv import load_dotenv

from rest_modules.users import Users
from utils import get_master_key, get_request_headers


load_dotenv()


class SessionOptions:
    def __init__(self, no_env_options: dict):
        self.user = Users(self)
        self.host = no_env_options.get("host", os.getenv("HOST"))
        self.api_key = no_env_options.get("api_key", os.getenv("API_KEY"))
        self.master_password = no_env_options.get("master_password", os.getenv("MASTER_PASSWORD"))
        self.use_master_password = True if self.master_password else False
        self.hash = "sha256"
        self.token = None
        self.refresh_token = None
        self.master_key = None
        self.request_headers = None
        self.user_info = None

    def login(self):
        self.token, self.refresh_token = self.user.login()

    def logout(self):
        self.user.logout()

    def get_user_info(self):
        self.user_info = self.user.get_user_info()

    def create_headers(self):
        mk_options = self.user.get_mk_options()
        self.master_key = get_master_key(mk_options, self.master_password) if mk_options.get("mkOptions") else None
        self.request_headers = get_request_headers(self.token, self.master_key, self.use_master_password)
