"""
Tests for requests.
"""
import responses
from unittest import TestCase

from xcovlib.registry import registry
from ..http_requests import HttpRequest
from ..generic import Request
from ..auth import SignatureAuth
from ..exceptions import AuthorizationError

class TestHttpRequest(TestCase):
    """
    Test the HttpRequest class.
    """
    def setUp(self):
        self.hostname = 'http://127.0.0.1:8000'
        self.partner_code = 'XCOV'
        self.key = 'XCOVAPIKEY'
        self.secret = 'xcovsecret'
        self.headers = {'header-1': 'value-1', 'header-2': 'value-2'}
        self.auth = SignatureAuth(self.key, self.secret)

        conn = HttpRequest(self.hostname, auth=self.auth)
        registry.setup({'http_handler': conn})

    @responses.activate
    def test_anonymous_requests(self):
        """
        Test a failing request with random auth data
        """
        responses.add(
            responses.GET,
            "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code),
            status=401
        )

        h = HttpRequest(self.hostname, auth=self.auth)
        with self.assertRaises(AuthorizationError):
            h.get('/api/v2/partners/{}/'.format(self.partner_code))


    @responses.activate
    def test_auth(self):
        """Test authenticated requests."""
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code),
                body='{}', content_type="application/json"
            )
            path = "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code)
            req = HttpRequest(self.hostname, auth=self.auth)
            req.get(path)       # Succeeds!

    @responses.activate
    def test_create(self):
        with responses.RequestsMock() as rsps:
            h = HttpRequest(self.hostname, auth=self.auth)
            # create a project
            path = '/api/v2/projects/'
            rsps.add(responses.POST,
                     "{}/api/v2/projects/".format(self.hostname),
                     status=201)
            data = {"slug": 'txlib', "name":'Txlib project'}
            h.post(path, data=data)

    @responses.activate
    def test_get_call_method(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code),
                body='yeahyouwork', content_type="application/json"
            )

            path = "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code)
            req = Request()
            resp = req.call('GET', path)  # Succeeds!
            self.assertEqual(resp, 'yeahyouwork')

    @responses.activate
    def test_post_call_method(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code),
                body='yeahyouwork', content_type="application/json"
            )

            path = "{}/api/v2/partners/{}/".format(self.hostname, self.partner_code)
            req = Request()
            resp = req.call('POST', path)  # Succeeds!
            self.assertEqual(resp, 'yeahyouwork')
