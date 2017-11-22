import csv
from abc import ABCMeta, abstractmethod
from typing import List, Type
from io import TextIOWrapper
from tweetstake.apps.common.decorators import singleton
from tweetstake.apps.csv.api import T
from tweetstake.apps.common.util import Constants, InfoException


class ICsvDAO(metaclass=ABCMeta):

    @abstractmethod
    def read_objects_list(self, session: TextIOWrapper, domain_class: Type[T]) -> List[T]:
        """
        Obtain objects of the domain model class from a csv file session
        :param session: TextIOWrapper object
        :param domain_class: domain model class
        :return: list of objects of the domain model class
        """


@singleton
class CsvDAO(ICsvDAO):

    def read_objects_list(self, session: TextIOWrapper, domain_class: Type[T]) -> List[T]:
        reader: any
        count_row: int = 0
        result: List[T] = list()
        domain_attributes: List[str] = list()

        with session as csv_file:
            reader = csv.reader(csv_file, delimiter=Constants.PARAMETER_CSV_DELIMITER,
                                quotechar=Constants.PARAMETER_CSV_QUOTECHAR,
                                skipinitialspace=Constants.PARAMETER_CSV_SKIPINITIALSPACE)
            for row in reader:
                if count_row == 0:
                    self.__validate_domain(domain_class, row)
                    domain_attributes = row
                else:
                    result.append(self.__deserialize(domain_class, domain_attributes, row))
                count_row += 1

        return result

    def __validate_domain(self, domain_class: Type[T], fields_list: List[str]) -> None:
        domain_object = domain_class()
        domain_attributes_list: List[str] = list(domain_object.__dict__.keys())
        if not all(x in fields_list for x in domain_attributes_list):
            raise InfoException(Constants.MSG_EXCEPTION_DOMAIN_ATTRIBUTES_NOT_MATCH_CSV_FIELDS)

    def __deserialize(self, domain_class: Type[T], domain_attributes: List[str], row: List) -> T:
        domain_object: T
        count_attribute: int

        domain_object = domain_class()
        count_attribute = 0
        for attr in domain_attributes:
            setattr(domain_object, attr, row[count_attribute])
            count_attribute += 1

        return domain_object