"""Enterprise manager module."""
import re
import json

from datetime import datetime
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE)
from uc3m_consulting.json_store import DocumentsJsonStore, NumDocsJsonStore
from uc3m_consulting.numdocs_report import NumDocsReport
from uc3m_consulting.starting_date import StartingDate
from uc3m_consulting.department import Department
from uc3m_consulting.project_acronym import ProjectAcronym
from uc3m_consulting.project_description import ProjectDescription
from uc3m_consulting.project_budget import ProjectBudget

class EnterpriseManager:
    """Main class for managing enterprise projects."""
    def __init__(self):
        pass

    @staticmethod
    def load_json_store(file_path):
        """Loads a JSON store file and returns its contents as a list"""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    @staticmethod
    def save_json_store(file_path, data_list):
        """Saves a list to a JSON store file"""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    @staticmethod
    def validate_cif(cif_code: str):
        """validates a cif number """
        if not isinstance(cif_code, str):
            raise EnterpriseManagementException("CIF code must be a string")
        cif_pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_pattern.fullmatch(cif_code):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letter = cif_code[0]
        cif_digits = cif_code[1:8]
        control_char = cif_code[8]

        odd_sum = 0
        even_sum = 0

        for i in range(len(cif_digits)):
            if i % 2 == 0:
                x = int(cif_digits[i]) * 2
                if x > 9:
                    odd_sum = odd_sum + (x // 10) + (x % 10)
                else:
                    odd_sum = odd_sum + x
            else:
                even_sum = even_sum + int(cif_digits[i])

        total_sum = odd_sum + even_sum
        units_digits = total_sum % 10
        control_number = 10 - units_digits

        if control_number == 10:
            control_number = 0

        control_letters = "JABCDEFGHI"

        if cif_letter in ('A', 'B', 'E', 'H'):
            if str(control_number) != control_char:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_letter in ('P', 'Q', 'S', 'K'):
            if control_letters[control_number] != control_char:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True

    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """registers a new project"""
        self.validate_cif(company_cif)
        ProjectAcronym(project_acronym)
        ProjectDescription(project_description)
        Department(department)
        StartingDate(date)
        ProjectBudget(budget)

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        projects_list = self.load_json_store(PROJECTS_STORE_FILE)

        for project_item in projects_list:
            if project_item == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        projects_list.append(new_project.to_json())

        self.save_json_store(PROJECTS_STORE_FILE, projects_list)
        return new_project.project_id


    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        self.parse_date(date_str)

        documents_store = DocumentsJsonStore()
        documents_list = documents_store.find_by_date(date_str)
        documents_count = documents_store.count_valid_documents(documents_list)

        if documents_count == 0:
            raise EnterpriseManagementException("No documents found")

        self.save_numdocs_report(date_str, documents_count)

        return documents_count

    @staticmethod
    def parse_date(date_str):
        """Parses and validates a date string in dd/mm/yyyy format"""
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        match_result = date_pattern.fullmatch(date_str)
        if not match_result:
            raise EnterpriseManagementException("Invalid date format")

        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

    @staticmethod
    def save_numdocs_report(date_str, documents_count):
        """Creates and stores the numdocs report entry"""
        report_entry = NumDocsReport(date_str, documents_count).to_json()
        numdocs_store = NumDocsJsonStore()
        numdocs_store.add_item(report_entry)
