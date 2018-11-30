from xcovlib.http.auth import SignatureAuth
from xcovlib.http.http_requests import HttpRequest
from xcovlib.registry import registry
from unittest import TestCase
from ..policytypes import PolicyTypes


class TestPolicyTypes(TestCase):

    def setUp(self):
        credentials = SignatureAuth(key='XCOVAPIKEY', secret='testsecret')
        host = '127.0.0.1:8001'
        conn = HttpRequest(host, auth=credentials)
        registry.setup({'http_handler': conn})

    def test_policy_types(self):
        types = PolicyTypes.get_policies()
        self.assertEqual(types.results[0]['name'], 'landlord_insurance')
        self.assertEqual(types.results[1]['name'], 'parcel_insurance')
