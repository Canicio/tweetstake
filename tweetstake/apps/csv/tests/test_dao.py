import unittest
from typing import Any, List
from unittest import mock
from unittest.mock import Mock

from io import TextIOWrapper, BufferedIOBase

from tweetstake.apps.csv.dao import CsvDAO


class CsvDAOTest(unittest.TestCase):

    def setUp(self) -> None:

        # Instantiate test class
        self.csv_dao: CsvDAO = CsvDAO()

    @mock.patch('tweetstake.apps.csv.dao.CsvDAO._CsvDAO__deserialize')
    @mock.patch('tweetstake.apps.csv.dao.CsvDAO._CsvDAO__validate_domain')
    @mock.patch('csv.reader')
    def test_read_objects_list(self, mocked_csv_reader_method: Mock, mocked_validate_domain_method: Mock,
                               mocked_deserialize_method: Mock) -> None:

        # Mock CSV API methods
        mocked_csv_reader_method.return_value = TestHelper.get_list_of_lists()

        # Mock PRIVATE methods
        mocked_validate_domain_method.return_value = None
        mocked_deserialize_method.return_value = DomainClassHelper()

        # Asserts
        result = self.csv_dao.read_objects_list(TextIOWrapper(buffer=BufferedIOBase()), DomainClassHelper)
        mocked_csv_reader_method.assert_called_once()
        mocked_validate_domain_method.assert_called_once_with(DomainClassHelper, ['field1', 'field2', 'field3'])
        mocked_deserialize_method.assert_called_once_with(DomainClassHelper, ['field1', 'field2', 'field3'],
                                                          ['value1', 'value2', 'value3'])
        self.assertEqual(1, len(result))
        self.assertTrue(hasattr(result[0], 'field1'))
        self.assertTrue(hasattr(result[0], 'field2'))
        self.assertTrue(hasattr(result[0], 'field3'))
        self.assertFalse(hasattr(result[0], 'field4'))
        self.assertTrue(result[0].field1 == 'value1')
        self.assertTrue(result[0].field2 == 'value2')
        self.assertTrue(result[0].field3 == 'value3')


class TestHelper(object):

    @staticmethod
    def get_list_of_lists() -> List[List]:
        list1: List = list()
        list2: List = list()
        list3: List = list()

        list1.append('field1')
        list1.append('field2')
        list1.append('field3')
        list2.append('value1')
        list2.append('value2')
        list2.append('value3')
        list3.append(list1)
        list3.append(list2)

        return list3


class DomainClassHelper(object):

    def __init__(self) -> None:
        self.field1 = 'value1'
        self.field2 = 'value2'
        self.field3 = 'value3'
