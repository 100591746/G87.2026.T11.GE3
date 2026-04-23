"""Contains the class ProjectDescription"""
import re

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class ProjectDescription:
    """Class representing and validating a project description"""

    def __init__(self, description: str):
        self.__value = self.validate(description)

    @staticmethod
    def validate(description):
        """Validates the project description"""
        description_pattern = re.compile(r"^.{10,30}$")
        if not description_pattern.fullmatch(description):
            raise EnterpriseManagementException("Invalid description format")
        return description

    @property
    def value(self):
        """Returns the validated description"""
        return self.__value
