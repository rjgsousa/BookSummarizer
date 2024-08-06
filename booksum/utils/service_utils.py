import requests

_api_url_by_book_title = "http://localhost:8001/summarize/"
_api_url_by_book_passage = "http://localhost:8001/summarize_text/"


def book_summary_api(data=None, given: str = None):
    types = ["book-title", "book-passage"]

    if given not in types:
        raise ValueError(f"{given} is not part of {types}")

    if given == 'book-title':
        _api_url = _api_url_by_book_title
    else:
        _api_url = _api_url_by_book_passage

    # make request
    response = requests.post(_api_url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        # todo: should raise an error
        return None
