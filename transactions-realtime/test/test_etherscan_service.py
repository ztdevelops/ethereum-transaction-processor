import unittest
from unittest.mock import patch

from service.etherscan_service import EtherscanService


class TestEtherscanService(unittest.TestCase):

    def setUp(self):
        self.api_key = "mock_api_key"
        self.etherscan_service = EtherscanService(self.api_key)

    @patch('utils.rest_util.RestUtil.get')
    def test_retrieves_contract_abi_successfully(self, mock_get):
        mock_response = {"status": "1", "message": "OK", "result": "mock_abi"}
        mock_get.return_value = mock_response

        response = self.etherscan_service.get_contract_abi("0xMockAddress")
        self.assertEqual(response, mock_response)

    @patch('utils.rest_util.RestUtil.get')
    def test_handles_api_failure(self, mock_get):
        mock_get.return_value = None

        response = self.etherscan_service.get_contract_abi("0xMockAddress")
        self.assertIsNone(response)

    @patch('utils.rest_util.RestUtil.get')
    def test_handles_empty_response(self, mock_get):
        mock_response = {"status": "0", "message": "No ABI found", "result": ""}
        mock_get.return_value = mock_response

        response = self.etherscan_service.get_contract_abi("0xMockAddress")
        self.assertEqual(response, mock_response)


if __name__ == '__main__':
    unittest.main()
