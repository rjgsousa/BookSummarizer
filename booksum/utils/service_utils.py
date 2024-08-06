import requests

_api_url = "http://localhost:8001/summarize/"


def book_summary_api(data=None):
    # make request
    response = requests.post(_api_url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        # todo: should raise an error
        return None
