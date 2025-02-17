# Riot Cookie Login

[Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)

## Use Examples

```python
import requests
import json

data = {
    'tdid': 'riot_account_cookie',
    'ssid': 'riot_account_cookie',
    'sub': 'riot_account_cookie',
    'csid': 'riot_account_cookie',
    'clid': 'riot_account_cookie'
}

response = requests.post("http://localhost/cookie_login", json=data)

if response.status_code == 200:
    print("Access Token:", response.json()['access_token'])
else:
    print(f"Error: {response.status_code}, {response.json()}")

```
