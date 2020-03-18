import contextlib
import responses
import unittest

from flask import template_rendered

from src import create_app
from src.codewars.utils import STATS_ENDPOINT
from src.github.utils import REPOS_ENDPOINT


@contextlib.contextmanager
def captured_templates(app):
    """Context manager to help determine which templates were rendered"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class MainTestCase(unittest.TestCase):
    """Class with basic tests."""

    mock_repos = [
        {
            'name': 'repo1',
            'html_url': 'https://github.com/username/repo1',
            'description': 'First repo of user',
        },
        {
            'name': 'repo2',
            'html_url': 'https://github.com/username/repo2',
            'description': 'Last repo of user',
        }
    ]

    mock_codewars_stats = {
        'leaderboardPosition': 420,
        'codeChallenges': {
            'totalAuthored': 1,
            'totalCompleted': 77,
        },
        'ranks': {
            'overall': {
                'name': '3 kyu',
            },
            'languages': {
                'python': {
                    'name': '4 kyu',
                    'score': 9000,
                }
            }
        }
    }

    def setUp(self):
        """Set up test environment."""
        super(MainTestCase, self).setUp()
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app
        self.test_client = app.test_client()
        self.assertEqual(app.debug, False)

        responses.add(responses.GET, REPOS_ENDPOINT,
                      json=self.mock_repos,
                      status=200)
        responses.add(responses.GET, STATS_ENDPOINT,
                      json=self.mock_codewars_stats,
                      status=200)

    def assertTemplateCalled(self, route, template_name, templates):
        _ = self.test_client.get(route, follow_redirects=True)
        template, context = templates[-1]
        self.assertEqual(template_name, template.name)

    @responses.activate
    def test_correct_template_is_loaded(self):
        """Checks that the template for displaying data is loaded"""
        app_routes = {
            '/': 'github_repos.html',
            '/codewars': 'codewars.html',
        }
        with captured_templates(self.app) as templates:
            for route, template_name in app_routes.items():
                self.assertTemplateCalled(
                    route=route,
                    template_name=template_name,
                    templates=templates
                )

    @responses.activate
    def test_html_contains_personal_information(self):
        """Test template is rendered with 'personal information' string."""
        response = self.test_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Information', response.data)
