"""Contains the class ProjectAcronym"""
import re

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class ProjectAcronym:
    """Class representing and validating a project acronym"""

    def __init__(self, acronym: str):
        self.__value = self.validate(acronym)

    @staticmethod
    def validate(acronym):
        """Validates the project acronym"""
        acronym_pattern = re.compile(r"^[a-zA-Z0-9]{5,10}")
        if not acronym_pattern.fullmatch(acronym):
            raise EnterpriseManagementException("Invalid acronym")
        return acronym

    @property
    def value(self):
        """Returns the validated acronym"""
        return self.__value
