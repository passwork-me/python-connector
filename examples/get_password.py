import json
import os.path

from loguru import logger
from passwork_api import PassworkAPI


# A way to overwrite the specified data in environment variables or not use environment variables at all
options_override = {
    # "host": "https://.../api/v4",
    # "api_key": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    # "master_password": "master_password",
}

api = PassworkAPI(options_override=options_override)
api.login()

PASSWORD_ID = "0123456789abcdefghijklmn"
DOWNLOAD_ATTACHMENTS_PATH = os.path.join("../downloaded_attachments", PASSWORD_ID)

# get password item
password_item = api.get_password(password_id=PASSWORD_ID)

# get vault id and vault item
vault_id = password_item.get("vaultId")
vault_item = api.get_vault(vault_id=vault_id)

# get vault password and password encryption key
vault_password = api.get_vault_password(vault_item=vault_item)
password_encryption_key = api.get_password_encryption_key(
    password_item=password_item, vault_password=vault_password
)

# get password customs
password_item["custom"] = api.get_customs(
    password_item=password_item, password_encryption_key=password_encryption_key
)

# download password attachments
api.get_attachments(
    password_item=password_item,
    password_encryption_key=password_encryption_key,
    download_path=DOWNLOAD_ATTACHMENTS_PATH,
)

# get password plain text
password_plain_text = api.get_password_plain_text(
    password_item=password_item, password_encryption_key=password_encryption_key
)

# receive full password info
full_password_info = {
    "password": password_item,
    "vault": vault_item,
    "vaultMasterKey": vault_password,
    "passwordMasterKey": password_encryption_key,
    "passwordPlainText": password_plain_text,
}

pretty_data = json.dumps(full_password_info, indent=4)
logger.success(pretty_data)

api.logout()
