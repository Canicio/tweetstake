import unittest
from typing import List
from unittest import mock
from unittest.mock import Mock, mock_open
from tweetstake.apps.csv.service import CsvService


class CsvServiceTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.csv_service: CsvService = CsvService()

    @mock.patch("builtins.open", new_callable=mock_open, read_data="data")
    @mock.patch('tweetstake.apps.csv.dao.CsvDAO.read_objects_list')
    def test_read_objects_list(self, mocked_read_objects_list_method: Mock, mock_file: Mock) -> None:

        result: List[object]

        # Mock DAO methods
        mocked_read_objects_list_method.return_value = [object, object]

        # Asserts
        result = self.csv_service.read_objects_list("path/to/open", object)
        mock_file.assert_called_once_with("path/to/open", 'r')
        self.assertEqual([object, object], result)
