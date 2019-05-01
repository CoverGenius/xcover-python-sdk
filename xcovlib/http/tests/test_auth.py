import os
from unittest import TestCase

from freezegun import freeze_time

from ..auth import SignatureAuth

os.environ['TZ'] = 'Europe/London'


class TestAuth(TestCase):

    @freeze_time("2019-01-01", tz_offset=0)
    def test_signature_auth_headers(self):
        key, secret = 'abcd', 'efgh'

        headers = SignatureAuth(key, secret).sign()
        self.assertEqual(headers['Authorization'],
                         'Signature keyId="abcd",algorithm="hmac-sha512",signature="f6RnwuCiDBJiAgi7fbc4cXEeKF%2BPKiIA%2BQbKVHqQmu3KHemhLg2wV5FDceUEbzPurmnqQi5H7W9Ot1om0o7W3A%3D%3D"')
        self.assertEqual(headers['Date'], 'Tue, 01 Jan 2019 00:00:00 GMT')
        self.assertEqual(headers['X-Api-Key'], 'abcd')
