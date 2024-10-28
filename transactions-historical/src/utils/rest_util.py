import requests


class RestUtil:
    """
    A static class to handle HTTP requests (GET, POST, PUT, DELETE).
    """

    @staticmethod
    def get(url: str, params: dict = None, headers: dict = None):
        """
        Send a GET request to the specified URL with optional parameters and headers.

        Args:
            url (str): The URL to send the GET request to.
            params (dict, optional): The query parameters to include in the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            dict or None: The JSON response if the status code is 200, otherwise None.
        """
        response = requests.get(url, params=params, headers=headers)
        return response.json() if response.status_code == 200 else None
