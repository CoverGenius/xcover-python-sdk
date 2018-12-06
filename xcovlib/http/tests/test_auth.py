from unittest import TestCase
from ..auth import SignatureAuth


class TestAuth(TestCase):
    def test_signature_auth_headers(self):
        """
        Test the signature generated is correct
        :return:
        """
        key, secret = 'abcd', 'efgh'
        auth_info = SignatureAuth(key, secret)

        host = 'xcover.com'
        method = 'POST'
        path = '/api/v2/quotes'

        auth_info.sign(path, host, method)
        self.assertEqual(
            {
                'Authorization': 'Signature algorithm="hmac-sha256",headers="(request-target) host x-api-key",signature="aTU90zZGMJRkz4OLiC1g0Z0V1VGn36qq+mWz85fVTdY="',
                'X-Api-Key': 'abcd'
            },
            auth_info._headers
        )
