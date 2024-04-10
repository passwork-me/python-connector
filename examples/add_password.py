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
VAULT_ID = "0123456789abcdefghijklmn"

vault_id = VAULT_ID if VAULT_ID else api.get_password(password_id=PASSWORD_ID)["vaultId"]
vault_item = api.get_vault(vault_id=vault_id)
vault_password = api.get_vault_password(vault_item=vault_item)

password_adding_fields = {
    "vaultId": vault_id,
    "name": "test",
    "url": "https://passwork.com",
    "login": "PassLogin",
    "description": "Password for testing",
    "folderId": None,
    "password": "password",
    "shortcutId": None,
    "tags": [],
    "snapshot": None,
    "color": "3",
    "custom": [
        {
          "name": "Additional login 1",
          "value": "PassLogin1",
          "type": "text"
        },
        {
          "name": "Additional password 1",
          "value": "password1",
          "type": "password"
        },
        {
          "name": "TOTP 1",
          "value": "JBSWY3DPEHPK3PXP",
          "type": "totp"
        }
    ],
    "attachments": [
        {
            "path": "../upload_attachments/file1.svg",
            "name": "file1.svg"
        },
        {
            "path": "../upload_attachments/file2.png",
            "name": "file2.png"
        }
    ]
}

added_password_info = api.add_password(password_adding_fields, vault_item, vault_password)
logger.success(f"Password with id {added_password_info['id']} has been added")

api.logout()
