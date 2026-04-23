"""Contains the class ProjectBudget"""
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class ProjectBudget:
    """Class representing and validating a project budget"""

    def __init__(self, budget):
        self.__value = self.validate(budget)

    @staticmethod
    def validate(budget):
        """Validates the project budget"""
        try:
            budget_float = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        budget_str = str(budget_float)
        if '.' in budget_str:
            decimals = len(budget_str.split('.')[1])
            if decimals > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if budget_float < 50000 or budget_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return budget

    @property
    def value(self):
        """Returns the validated budget"""
        return self.__value
