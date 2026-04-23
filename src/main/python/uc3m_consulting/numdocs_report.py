"""Contains the class NumDocsReport"""
from datetime import datetime, timezone


class NumDocsReport:
    """Class representing the numdocs report entry"""

    def __init__(self, query_date: str, num_files: int):
        self.__query_date = query_date
        self.__report_date = datetime.now(timezone.utc).timestamp()
        self.__num_files = num_files

    def to_json(self):
        """Returns the object data in json format"""
        return {
            "Querydate": self.__query_date,
            "ReportDate": self.__report_date,
            "Numfiles": self.__num_files
        }