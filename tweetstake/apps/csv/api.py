from abc import ABCMeta, abstractmethod
from typing import TypeVar, List

T = TypeVar('T')


class ICsv(metaclass=ABCMeta):

    @abstractmethod
    def read_objects_list(self, file: str, domain: T) -> List[T]:
        """
        Obtain objects of the domain model class from a csv file
        :param file: csv file path
        :param domain: domain model class
        :return: list of objects of the domain model class
        """
