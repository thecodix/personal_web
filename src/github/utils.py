import requests

GITHUB_API_URL = 'https://api.github.com/users/thecodix'
REPOS_ENDPOINT = f'{GITHUB_API_URL}/repos'


def fetch_from_github_api(endpoint):
  """Retrieves data from a github api endpoint

  :param str endpoint: url to fetch from
  :return: yields resources from the endpoint
  :raises:
  RequestException: If Github API is unreachable or returns 400/404 code.
  """
  response = requests.get(endpoint)
  if response.status_code != 200:
    raise requests.exceptions.RequestException()
  yield from response.json()


def github_repositories():
    """Yields repositories from the Github endpoint /repos"""
    yield from fetch_from_github_api(REPOS_ENDPOINT)


def get_repos():
    """Lists repositories info from Github."""
    repos = []
    for repo in github_repositories():
      info = {
        'name': repo['name'],
        'url': repo['html_url'],
        'description': repo['description'],
      }
      repos.append(info)
    return repos
