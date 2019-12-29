import openpyxl
import os

from main_window import ERRORS


class DocFile:
    def __init__(self):
        self.files_list = self.get_files_list()
        self.file_name = ""
        self.sheet_name: ""
        self.sheets_list = list()

    # Получение списка табличных файлов в текущей директории
    @staticmethod
    def get_files_list():
        path = os.getcwd()
        file_list = list()
        for elem in os.listdir(path):
            if os.path.isfile(elem) and elem.endswith((".xls", ".xlsx")):
                file_list.append(elem)
        file_list.sort()
        return file_list

    # Проверка существования файла. Чтение списка листов в файле
    def get_sheets_list(self, file_name: str) -> (list, str):
        if os.path.isfile(file_name):
            self.file_name = file_name
            # TODO: получение списка листов показанного документа и добавление списка в атрибут класса (self.all_sheets)
            wb = openpyxl.load_workbook(file_name)
            return wb.sheetnames, ""
        return list(), ERRORS['no_file']

    def is_sheet_exist(self, sheet_name):
        if sheet_name in self.sheets_list:
            # TODO: проверка существования листов
            pass

    def get_cell_row(self, text_in_cell):
        pass


def test(file_name):

    print(os.path.isfile(file_name))
    wb = openpyxl.load_workbook(file_name)
    sheets = wb.sheetnames
    print(sheets)


if __name__ == "__main__":
    print(os.getcwd())
    test('table.xlsx')


