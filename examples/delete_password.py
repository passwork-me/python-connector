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
api.delete_password(password_id=PASSWORD_ID)

api.logout()
