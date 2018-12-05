from xcovlib.registry import registry


class Request:
    """
    A generic request class to call Endpoints directly incase the
    API Model for such a resource does not exist yet
    """
    def __init__(self):
        self._http = registry.http_handler

    def call(self, method, path, data=None, **kwargs):
        """
        Method that calls the endpoint and returns the results
        :param method: GET, POST, PUT etc
        :param path: The URL where the endpoint needs to hit
        :param data: The payload or data that needs to be passed, can be None
        :param kwargs: Any other header values, pass headers like headers = {'key': 'value', 'key1': 'value1'}
        :return:
        """
        return self._http._make_request(method, path, data, **kwargs)
