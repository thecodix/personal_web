"""Application routes"""
import requests
from flask import render_template

from src.github import utils
from src.codewars import utils as codewars_utils
from . import personal_bp


@personal_bp.route('/')
def main_view():
    """Displays github repos"""
    try:
        repos_list = utils.get_repos()
        return render_template('github_repos.html', repos=repos_list, errors=False)
    except requests.exceptions.RequestException:
        return render_template('github_repos.html', errors=True)


@personal_bp.route('/codewars')
def codewars_view():
    """Displays codewars stats"""
    try:
        codewars_stats = codewars_utils.get_codewars_info()
        return render_template('codewars.html',
                               codewars=codewars_stats,
                               errors=False)
    except requests.exceptions.RequestException:
        return render_template('codewars.html', errors=True)
