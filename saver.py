import xlsxwriter
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
    def is_file_exist(self, file_name: str) -> (bool, str):
        print(file_name)
        if os.path.isfile(file_name):
            self.file_name = file_name
            # TODO: получение списка листов показанного документа и добавление списка в атрибут класса (self.all_sheets)
            return True, ""
        return False, ERRORS['no_file']

    def is_sheet_exist(self, sheet_name):
        if sheet_name in self.sheets_list:
            # TODO: проверка существования листов
            pass

    def get_cell_row(self, text_in_cell):
        pass


def test(file_name):

    print(os.path.isfile(file_name))
    f = xlsxwriter.Workbook(file_name)
    new_sheet = f.add_chartsheet("test_create_sheet_60")


if __name__ == "__main__":
    print(os.getcwd())
    test('2020.odt')
    test('2019.xls')
    test('2018.xls')

