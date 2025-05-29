import requests


def make_request(endpoint):
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)
        return None
