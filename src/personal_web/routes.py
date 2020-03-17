"""Application routes"""
import requests
from flask import render_template

from src.github import utils
from . import personal_bp


@personal_bp.route('/')
def main_view():
    """Displays github repos"""
    try:
        repos_list = utils.get_repos()
        return render_template('github_repos.html', repos=repos_list, errors=False)
    except requests.exceptions.RequestException:
        return render_template('github_repos.html', errors=True)
