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

    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None):
        """
        Send a POST request to the specified URL with optional data and headers.

        Args:
            url (str): The URL to send the POST request to.
            data (dict, optional): The JSON data to include in the request body. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            dict or None: The JSON response if the status code is 200, otherwise None.
        """
        response = requests.post(url, json=data, headers=headers)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None):
        """
        Send a PUT request to the specified URL with optional data and headers.

        Args:
            url (str): The URL to send the PUT request to.
            data (dict, optional): The JSON data to include in the request body. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            dict or None: The JSON response if the status code is 200, otherwise None.
        """
        response = requests.put(url, json=data, headers=headers)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def delete(url: str, headers: dict = None):
        """
        Send a DELETE request to the specified URL with optional headers.

        Args:
            url (str): The URL to send the DELETE request to.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            bool: True if the status code is 200, otherwise False.
        """
        response = requests.delete(url, headers=headers)
        return response.status_code == 200