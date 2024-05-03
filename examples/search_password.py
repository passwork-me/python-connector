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

search_params = {
    "query": "test",
    "tags": [],
    "colors": [],
    "vaultId": None,
    "includeShared": False,
    "includeShortcuts": False,
}

found_passwords = api.search_password(**search_params)
if found_passwords:
    found_passwords_ids = [found_password["id"] for found_password in found_passwords]
    logger.success(f"Found password IDs: {', '.join(found_passwords_ids)}")
    for numb, found_password in enumerate(found_passwords):
        logger.success(f"Found password #{numb+1}/{len(found_passwords)}: {found_password}")

api.logout()
