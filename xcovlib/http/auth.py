"""
Authentication related module.
"""
from __future__ import unicode_literals

import hmac
import re
from base64 import b64encode
from hashlib import sha1
from urllib.parse import quote

from ..utils.dates import http_date

SIGNATURE_RE = re.compile('signature="(.+?)"')


class SignatureAuth(object):
    """Class for basic authentication support."""

    def __init__(self, key, secret):
        self._key = key
        self._secret = secret
        self._headers = None

    def create_signature(self, date):
        raw = 'date: {date}'.format(date=date)
        hashed = hmac.new(self._secret.encode('utf-8'), raw.encode('utf-8'), sha1).digest()
        return quote(b64encode(hashed))

    def build_signature(self, signature, key):
        template = ('Signature keyId="%(key)s",algorithm="hmac-sha1",'
                    'signature="%(signature)s"')

        return template % {
            'key': key,
            'signature': signature
        }

    def sign(self):
        date = http_date()
        auth = self.build_signature(signature=self.create_signature(date), key=self._key)

        return {
            'Date': date,
            'Authorization': auth,
            'X-Api-Key': self._key,
        }
