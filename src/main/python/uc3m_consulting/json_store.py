"""JSON store classes"""
import json

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (
    TEST_DOCUMENTS_STORE_FILE,
    TEST_NUMDOCS_STORE_FILE
)


class JsonStore:
    """Generic JSON store"""

    def __init__(self, file_path):
        self._file_path = file_path

    def load(self):
        """Loads a JSON store file and returns its contents as a list"""
        try:
            with open(self._file_path, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format"
            ) from ex

    def save(self, data_list):
        """Saves a list to a JSON store file"""
        try:
            with open(self._file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex


class DocumentsJsonStore(JsonStore):
    """Manages the documents JSON store"""

    def __init__(self):
        super().__init__(TEST_DOCUMENTS_STORE_FILE)


class NumDocsJsonStore(JsonStore):
    """Manages the numdocs JSON store"""

    def __init__(self):
        super().__init__(TEST_NUMDOCS_STORE_FILE)