"""Contains the class StartingDate"""
import re
from datetime import datetime, timezone

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class StartingDate:
    """Class representing and validating a project starting date"""

    def __init__(self, date_str: str):
        self.__value = self.validate(date_str)

    @staticmethod
    def validate(date_str):
        """Validates the starting date"""
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        match_result = date_pattern.fullmatch(date_str)
        if not match_result:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return date_str

    @property
    def value(self):
        """Returns the validated date string"""
        return self.__value