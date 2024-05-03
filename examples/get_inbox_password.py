import os
import json
from loguru import logger
from passwork_api import PassworkAPI


# A way to overwrite the specified data in environment variables or not use environment variables at all
options_override = {
    # "host": "https://.../api/v4",
    # "api_key": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    # "master_password": "master_password",
}

# PASSWORD_ID = "0123456789abcdefghijklmn"
PASSWORD_ID = ""
DOWNLOAD_ATTACHMENTS_PATH = "../downloaded_attachments/"

api = PassworkAPI(options_override=options_override)
api.login()
api.get_user_info()

if not PASSWORD_ID:
    list_inbox_passwords = api.get_inbox_passwords()
    PASSWORD_ID = list_inbox_passwords[0]['id']

inbox_item = api.get_inbox_password(inbox_password_id=PASSWORD_ID)
encryption_key = api.get_inbox_encryption_key(inbox_item)
inbox_password_item = inbox_item["password"]

# get inbox password customs
inbox_password_item["custom"] = api.get_customs(
    password_item=inbox_password_item, password_encryption_key=encryption_key
)

# download inbox password attachments
api.get_attachments(
    password_item=inbox_password_item,
    password_encryption_key=encryption_key,
    download_path=os.path.join(DOWNLOAD_ATTACHMENTS_PATH, PASSWORD_ID),
)

# get inbox password plain text
password_plain_text = api.get_password_plain_text(
    password_item=inbox_password_item, password_encryption_key=encryption_key
)

# receive full inbox password info
inbox_password_info = {
    "inbox_item": inbox_item,
    "passwordPlainText": password_plain_text,
}

pretty_data = json.dumps(inbox_password_info, indent=4)
logger.success(pretty_data)

api.logout()
