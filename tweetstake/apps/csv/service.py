from typing import List, Type
from tweetstake.apps.common.decorators import singleton
from tweetstake.apps.csv.api import ICsv, T
from tweetstake.apps.common.util import Constants
from tweetstake.apps.csv.dao import CsvDAO


@singleton
class CsvService(ICsv):

    def read_objects_list(self, file: str, domain_class: Type[T]) -> List[T]:
        result: List[T]
        file_session = open(file, Constants.MODE_OPEN_FILE_R)
        result = CsvDAO().read_objects_list(file_session, domain_class)

        return result
