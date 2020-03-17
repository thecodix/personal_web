import contextlib
import unittest

from flask import template_rendered

from src import create_app


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

    def test_correct_template_is_loaded(self):
        """Checks that the template for displaying data is loaded"""
        with captured_templates(self.app) as templates:
            _ = self.test_client.get('/', follow_redirects=True)
            template, context = templates[0]
            self.assertEqual(template.name, 'github_repos.html')

    def test_html_contains_hello_world(self):
        """Test template is rendered with hello world message."""
        response = self.test_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World!', response.data)
