## About the API
Passwork API lets you retrieve, create, update passwords, folders and vaults. It is an easy way how you can integrate Passwork with your infrastructure. Use our Passwork Python Connector to make the integration smoother. The API operates behalf of the user whom API Key is used.
Check for all available methods in
[Passwork API Methods](./passwork_api.py)

## How to install
⚠️<b style='color:YELLOW'>WARNING</b> the connector will not work with python version less than <b>3.10</b>
```shell script
git clone https://github.com/passwork-me/python-connector.git .
pip install -r requirements.txt
```

## Environment variables
The following environment variables are required for operation:

<b>HOST:</b> The address of the API server, like `https://.../api/v4` <br>
<b>API_KEY:</b> Your API key for authentication, instructions for obtaining below <br>
<b>MASTER_PASSWORD:</b> Client-side encryption key. Only add it when client-side encryption is enabled <br>

Several available options for storing environment variables: <br>
1) [.env file](./.env)
2) run/debug configuration (IDLE)
3) system environment variables

### API Key

![alt text](./passwork.png)

- Sign in to your Passwork
- Menu → API Settings
- Enter your authorization key and generate the API Key

Use method `login()` on instance of [PassworkAPI class](./passwork_api.py) to retrieve a temporary API Token.
An API token is a session token. It is valid as long as you are accessing the API. After it expires, you will need to log in again.
API Token Lifetime can be set up in your Passwork.
The retrieved API token is stored as an instance variable named `session_options` within the [PassworkAPI class](./passwork_api.py) and is subsequently sent in an HTTP header.

## Step-by-step guide

### Create session (common step for all operations)
0. Create instance of API connection and open session. 
```python
from passwork_api import PassworkAPI

# A way to overwrite the specified data in environment variables or not use environment variables at all
options_override = {
    "host": str(),
    "api_key": str(),
    "master_password": str(),
}

api = PassworkAPI(options_override=options_override)
api.login()
# api.logout()  # close session after all operations with Passwork API
```

### [Password search by parameters](./examples/search_password.py)

1. Fill data in `search_params` dict template with searching parameters to `search_password` method

```python
search_params = {
    "query": "",
    "tags": [],
    "colors": [],
    "vaultId": None,
    "includeShared": False,
    "includeShortcuts": False,
}
```

2. Search password

```python
found_passwords = api.search_password(**search_params)
```


### [Get full password info](./examples/get_password.py)
<b style='color:green'>NOTE</b> `PASSWORD_ID` must contain the identifier of the target password, in the example a non-existent identifier is specified
1. Get password and vault items
```python
PASSWORD_ID = "0123456789abcdefghijklmn"
DOWNLOAD_ATTACHMENTS_PATH = os.path.join("../downloaded_attachments", PASSWORD_ID)

password_item = api.get_password(password_id=PASSWORD_ID)
vault_id = password_item.get("vaultId")
vault_item = api.get_vault(vault_id=vault_id)
```

2. Receive vault password and password encryption key

```python
vault_password = api.get_vault_password(vault_item=vault_item)
password_encryption_key = api.get_password_encryption_key(
    password_item=password_item,
    vault_password=vault_password,
    download_path=DOWNLOAD_ATTACHMENTS_PATH,
)
```

3. Receive password customs, password plain text and download attachments 

```python
password_item["custom"] = api.get_customs(
    password_item=password_item,
    password_encryption_key=password_encryption_key
)

api.get_attachments(
    password_item=password_item,
    password_encryption_key=password_encryption_key
)

password_plain_text = api.get_password_plain_text(
    password_item=password_item,
    password_encryption_key=password_encryption_key
)
```

4. Show full password info in readable format

```python
full_password_info = {
    "password": password_item,
    "vault": vault_item,
    "vaultMasterKey": vault_password,
    "passwordMasterKey": password_encryption_key,
    "passwordPlainText": password_plain_text,
}

pretty_data = json.dumps(full_password_info, indent=4)
logger.success(pretty_data)
```

### [Get inbox password info](./examples/get_inbox_password.py)
<b style='color:green'>NOTE</b> `PASSWORD_ID` must contain the identifier of the target password, in the example a non-existent identifier is specified. without explicitly specifying `PASSWORD_ID` the information for the last password in Inbox will be retrieved.

Steps are similar to the previous example ([get full password info](./examples/get_password.py)).


### [Add password](./examples/add_password.py)
<b style='color:green'>NOTE</b> If `VAULT_ID` is specified, the `PASSWORD_ID` variable may be empty.
Without specifying of `VAULT_ID`, the identifier of the vault where the password with id = `PASSWORD_ID` is stored will be taken. 
The identifiers `PASSWORD_ID` and `VAULT_ID` in the example are non-existent.

1. Receive vault item and vault password
```python
PASSWORD_ID = "0123456789abcdefghijklmn"
VAULT_ID = "0123456789abcdefghijklmn"

vault_id = VAULT_ID if VAULT_ID else api.get_password(password_id=PASSWORD_ID)["vaultId"]
vault_item = api.get_vault(vault_id=vault_id)
vault_password = api.get_vault_password(vault_item=vault_item)
```

2. Fill data in `password_adding_fields` dict template
```python
password_adding_fields = {}
```

3. Add password
```python
added_password_info = api.add_password(password_adding_fields, vault_item, vault_password)
logger.success(f"Password with id {added_password_info['id']} has been added")
```

### [Delete password](./examples/delete_password.py)
<b style='color:green'>NOTE</b> `PASSWORD_ID` must contain the identifier of the target password, in the example a non-existent identifier is specified

1. Delete a password by its id
```python
PASSWORD_ID = "0123456789abcdefghijklmn"
api.delete_password(password_id=PASSWORD_ID)
```

### Examples and algorithm of work with the connector
[Examples here](./examples)


### License
This project is licensed under the terms of the MIT license.
