import unittest
from unittest.mock import patch

from dto.historical_transaction_request_dto import HistoricalTransactionRequestDTO
from service.etherscan_service import EtherscanService


class TestEtherscanService(unittest.TestCase):

    def setUp(self):
        self.api_key = "mock_api_key"
        self.etherscan_service = EtherscanService(self.api_key)

    @patch('utils.rest_util.RestUtil.get')
    def test_retrieves_historical_data_successfully(self, mock_get):
        mock_response = {"status": "1", "message": "OK", "result": []}
        mock_get.return_value = mock_response

        request = HistoricalTransactionRequestDTO(
            address="0xMockAddress",
            page=1,
            offset=10,
            start_block=0,
            end_block=99999999
        )
        response = self.etherscan_service.get_historical_data(request)
        self.assertEqual(response, mock_response)

    @patch('utils.rest_util.RestUtil.get')
    def test_handles_api_failure(self, mock_get):
        mock_get.return_value = None

        request = HistoricalTransactionRequestDTO(
            address="0xMockAddress",
            page=1,
            offset=10,
            start_block=0,
            end_block=99999999
        )
        response = self.etherscan_service.get_historical_data(request)
        self.assertIsNone(response)

    @patch('utils.rest_util.RestUtil.get')
    def test_handles_empty_response(self, mock_get):
        mock_response = {"status": "0", "message": "No transactions found", "result": []}
        mock_get.return_value = mock_response

        request = HistoricalTransactionRequestDTO(
            address="0xMockAddress",
            page=1,
            offset=10,
            start_block=0,
            end_block=99999999
        )
        response = self.etherscan_service.get_historical_data(request)
        self.assertEqual(response, mock_response)


if __name__ == '__main__':
    unittest.main()
