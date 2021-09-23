import requests


class HttpClient:
    # The host to connect to.
    host = None

    # The access token for this request.
    access_token = None

    def __init__(self, host: str):
        """
        The HttpClient constructor.

        :param host:
        :type host: str
        """

        self.host = host

    def post(self, uri: str, with_access_token=False, **kwargs):
        """
        The post request.

        :param uri:
        :param with_access_token:
        :param kwargs:

        :return:
        """
        if with_access_token:
            return requests.post(self._url(uri), headers={'Authorization': 'Bearer ' + self.access_token}, **kwargs)

        return requests.post(self._url(uri), **kwargs)

    def get(self, uri, with_access_token=False, **kwargs):
        """
              The get request.

              :param uri:
              :param with_access_token:
              :param kwargs:

              :return:
        """
        if with_access_token:
            return requests.get(self._url(uri), headers={'Authorization': 'Bearer ' + self.access_token}, **kwargs)

        return requests.get(self._url(uri), **kwargs)

    def _url(self, uri: str):
        """
        The uri with the
        :param uri:
        :return:
        """
        return self.host + uri
