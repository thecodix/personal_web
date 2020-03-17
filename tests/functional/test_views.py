import unittest

from src import create_app


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

  def test_html_contains_hello_world(self):
    """Test template is rendered with hello world message."""
    response = self.test_client.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Hello World!', response.data)
