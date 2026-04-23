"""JSON store classes"""
from datetime import datetime
import json

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (
    TEST_DOCUMENTS_STORE_FILE,
    TEST_NUMDOCS_STORE_FILE,
)
from uc3m_consulting.project_document import ProjectDocument


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

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DocumentsJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            super().__init__(TEST_DOCUMENTS_STORE_FILE)
            self._initialized = True

    def find_by_date(self, date_str):
        """Returns the documents registered on the given date"""
        documents_list = self.load()
        documents_found = []

        for document in documents_list:
            time_val = document["register_date"]
            doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")
            if doc_date_str == date_str:
                documents_found.append(document)

        return documents_found

    @staticmethod
    def count_valid_documents(documents_list):
        """Validates the documents and returns how many are valid"""
        documents_count = 0

        for document in documents_list:
            ProjectDocument.build_from_store_data(document)
            documents_count = documents_count + 1

        return documents_count


class NumDocsJsonStore(JsonStore):
    """Manages the numdocs JSON store"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NumDocsJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            super().__init__(TEST_NUMDOCS_STORE_FILE)
            self._initialized = True

    def add_item(self, item):
        """Adds a new item to the numdocs store"""
        data_list = self.load()
        data_list.append(item)
        self.save(data_list)
