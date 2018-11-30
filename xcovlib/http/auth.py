"""
Authentication related module.
"""
from __future__ import unicode_literals

import re
from httpsig import HeaderSigner


SIGNATURE_RE = re.compile('signature="(.+?)"')


class SignatureAuth(object):
    """Class for basic authentication support."""

    def __init__(self, key, secret):
        """Initializer."""
        self._key = key
        self._secret = secret
        self._headers = None


    def create_signature(self, method, host, path):
        """
        Create the HMAC-SHA256 signature string for a particular set of request
        details. This is a hash of certain message details that is produced by the
        sender and reproduced by the receiver. The two hashes should then match.
        """
        unsigned = {
            'host': host.lower(),
            'x-api-key': self._key,
        }
        signer = HeaderSigner(
            key_id=self._key, secret=self._secret,
            headers=['(request-target)', 'host', 'x-api-key'], algorithm='hmac-sha256')
        signed = signer.sign(unsigned, method=method.upper(), path=path)
        signature = signed['authorization']

        match = SIGNATURE_RE.search(signature)

        if not match:
            return None
        return match.group(1)


    def build_signature(self, headers, signature):
        template = ('Signature algorithm="hmac-sha256",'
                    'headers="%(headers)s",signature="%(signature)s"')

        return template % {
            'signature': signature,
            'headers': ' '.join(headers),
        }


    def sign(self, path, method, host):
        signature = self.create_signature(method, host, path)

        headers = ['(request-target)', 'host', 'x-api-key']

        self._headers = {
            'Authorization': self.build_signature(headers, signature=signature),
            'X-Api-Key': self._key
        }
