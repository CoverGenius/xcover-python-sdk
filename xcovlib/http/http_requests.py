import json
import requests
from xcovlib.utils import _logger
from .base import BaseRequest
from .exceptions import NoResponseError


class HttpRequest(BaseRequest):
    """Basic http requests handler.

    This class can handle both HTTP and HTTPS requests.
    """

    def get(self, path):
        """Make a GET request.

        Args:
            `path`: The path to the resource.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return json.loads(self._make_request('GET', path))

    def post(self, path, data):
        """Make a POST request.

        The data is JSON-Encoded

        Args:
            `path`: The path to the resource.
            `data`: The data to send. The data must already be JSON-encoded.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._send('POST', path, data)

    def put(self, path, data):
        """Make a PUT request.

        The data must already be JSON-encoded. We specify the Content-Type accordingly.


        Args:
            `path`: The path to the resource.
            `data`: The data to send. The data must already be JSON-encoded.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._send('PUT', path, data)

    def patch(self, path, data):
        """Make a PUT request.

        The data must already be JSON-encoded. We specify the Content-Type accordingly.

        Args:
            `path`: The path to the resource.
            `data`: The data to send. The data must already be JSON-encoded.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._send('PATCH', path, data)


    def _make_request(self, method, path, data=None, **kwargs):
        """Make a request.

        Use the `requests` module to actually perform the request.

        Args:
            `method`: The method to use.
            `path`: The path to the resource.
            `data`: Any data to send (for POST and PUT requests).
            `kwargs`: Other parameters for `requests`.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        _logger.debug("Method for request is %s" % method)
        url = self._construct_full_url(path)
        _logger.debug("URL for request is %s" % url)
        self._auth_info.sign(path, method, self.only_host)
        _logger.debug("The arguments are %s" % kwargs)

        # Add custom headers for the request
        if self._auth_info._headers:
            kwargs.setdefault('headers', {}).update(self._auth_info._headers)

        res = requests.request(method, url, data=data, verify=False, **kwargs)
        if res.ok:
            _logger.debug("Request was successful.")
            return res.content.decode('utf-8')

        if hasattr(res, 'content'):
            _logger.debug("Response was %s:%s", res.status_code, res.content)
            raise self._exception_for(res.status_code)(
                res.content.decode('utf-8'), http_code=res.status_code
            )
        else:
            msg = "No response from URL: %s" % res.request.url
            _logger.error(msg)
            raise NoResponseError(msg)

    def _send(self, method, path, data):
        """Send data to a remote server, either with a POST or a PUT request.

        Args:
            `method`: The method (POST or PUT) to use.
            `path`: The path to the resource.
            `data`: The data to send.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        headers = {'Content-type': 'application/json'}
        return self._make_request(method, path, data=data, headers=headers)
