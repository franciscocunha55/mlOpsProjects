import json

import requests


def request_url (url):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(response.json(), indent=2))
    values = data ['headers']['User-Agent']
    print(values)


if __name__ == '__main__':
    request_url("http://httpbin.org/headers")