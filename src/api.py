import requests


def perform_api_request(endpoint):
    """Performs an API get request to the endpoint provided

    :param str endpoint: url to fetch from
    :return: response from endpoint
    :raises:
    RequestException: If API endpoint is unreachable or returns 400/404 code.
    """
    response = requests.get(endpoint)
    if response.status_code != 200:
        raise requests.exceptions.RequestException()
    return response
