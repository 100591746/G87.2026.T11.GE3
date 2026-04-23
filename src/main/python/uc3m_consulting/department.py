"""Contains the class Department"""
import re

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class Department:
    """Class representing and validating a department"""

    def __init__(self, department: str):
        self.__value = self.validate(department)

    @staticmethod
    def validate(department):
        """Validates the department"""
        department_pattern = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        if not department_pattern.fullmatch(department):
            raise EnterpriseManagementException("Invalid department")
        return department

    @property
    def value(self):
        """Returns the validated department"""
        return self.__value