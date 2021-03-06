import json
import os
import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel

import saver
from messages.errors import ERRORS
from messages.status import STATUS
from py_windows.design import Ui_MainWindow

DATA = {}  # Загружается из json-файла при инициализации класса ExampleApp
JSON_FILE = 'name_list.json'
INPUT_FIELD_TYPE = QtWidgets.QLineEdit


class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.ui = Ui_MainWindow()
        self.file = saver.DocFile()

        # Это нужно для инициализации нашего дизайна
        self.ui.setupUi(self)

        # Кнопка вывода в консоль имен полей
        self.ui.pushButton.clicked.connect(self.print_fields)

        # Кнопка проверки введенных данных(+save +clear)
        self.ui.pushButton_2.clicked.connect(self.get_data_from_fields)

        # Кнопка очистки формы
        self.ui.pushButton_3.clicked.connect(self.clear_fields)

        # Инициализация выпадающего списка районов
        self.load_name_list(JSON_FILE)

        # Инициализация выпадающего списка файлов
        self.load_files_list()
        self.clear_fields()

    # Загрузка данных о Пожарных частях в районах
    def load_name_list(self, file_name):
        global DATA
        self.ui.box_area_1.addItem("-")  # Добавление первого (пустого) значения в выпадающий список
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                DATA = json.loads(f.read())
            self.ui.box_area_1.addItems(DATA.keys())

            # Уставнока сигнала для поля выбора района
            self.ui.box_area_1.currentIndexChanged.connect(self.get_point_list)

            # Сохранение списка всех имеющихся Пожарных частей (points) в атрибуте
            if not self.file.points_list:
                for values in DATA.values():
                    self.file.points_list.extend(values)

            # Заполенение текстового поля всеми имеющимися названиями Пожарных частей
            # TODO: сделать проверку и выборку и вывод в текстовое поле только тех пожарных частей,
            #  даннные по которым "незаполнены".

            # TODO: реализовать чтение заданной области из Excel-файла названий частей, которые "незаполнены".

            # TODO*: добавить изменение цвета в текстовом поле вывода "незаполенных" частей (рекомендуется)

            model = QStringListModel(self.file.points_list)

            self.ui.listView.setModel(model)
        else:
            self.show_error_text(ERRORS["no_name_list"])

    # Сборка выпадающего списка исходя из того, какой выбран район.
    def get_point_list(self):
        self.ui.box_point_1.clear()
        self.ui.box_point_1.addItem("-")
        selected_area = self.ui.box_area_1.currentText()
        for area, point_list in DATA.items():
            if selected_area == area:
                self.ui.box_point_1.addItems(point_list)

    # служебная функция для просмотра подключенных виджетов TODO: удалить после завершения
    def print_fields(self):
        for elem in self.ui.__dict__.items():
            print(elem)

    # Очистка всех полей формы и заполенение их нулями.
    def clear_fields(self):
        self.clear_message()
        for field_name, field_type in self.ui.__dict__.items():
            if isinstance(field_type, INPUT_FIELD_TYPE):
                self.ui.__dict__[field_name].setText('0')

    # Возвращает value преобразованное в число, либо "error" и выводит ошибку
    def give_me_int(self, value: str) -> int or str:
        try:
            return int(value)
        except ValueError:
            self.show_error_text(ERRORS["not_number"])
            return "error"

    # Получение данных со всех полей ввода и приведение их к числам.
    # В случае корректности, поля очищаются.
    def get_data_from_fields(self) -> list or None:
        self.ui.label_error.setText("")
        data = []
        for field_name, field_type in self.ui.__dict__.items():
            if isinstance(field_type, INPUT_FIELD_TYPE):
                field_text = self.ui.__dict__[field_name].text()
                data.append(self.give_me_int(field_text))
        if "error" in data:
            return None

        # Проверка, на то, что пользватель ввел только нули (пустая форма)
        elif not any(data):
            self.show_status_text(STATUS['is_empty'])

        else:
            err = self.save_input_data(data)
            if err is None:
                self.clear_fields()
                self.show_status_text(STATUS['is_valid'])
            else:
                self.show_error_text(error=err)

            # print(data)

    # Функция нициализации выпадающего списка файлов и связывание с выпадающим списком листов в документе
    def load_files_list(self):
        files_list = self.file.get_files_list()
        files_list.insert(0, "-")

        # Составление выпадающего списка файлов
        self.ui.box_file_1.addItems(files_list)

        # Добавление сигнала в поле списка файлов. Через lambda реализована передача параметра с именем,
        # которое выбирает пользователь с списке файлов в текущей директории
        self.ui.box_file_1.currentTextChanged.connect(
            lambda val=self.get_select_element("box_file_1"): self.load_sheets_list(val)
        )

    def load_sheets_list(self, file_name: str):
        self.ui.box_sheet_1.clear()
        sheets_list, error = self.file.get_sheets_list(file_name)
        self.ui.box_sheet_1.addItem("-")  # Закоммитить эту строчку. чтобы последняя вкладка выбиралась автоматически.
        if error:
            self.show_error_text(error)
        elif len(sheets_list) == 0:
            self.show_error_text(ERRORS['no_sheets'])
        else:
            sheets_list.sort(reverse=True)     # Сортировка листов документа в обратном порядке.
            self.ui.box_sheet_1.addItems(sheets_list)

            # Добавление сигнала в поле списка файлов. Через lambda реализована передача параметра с именем,
            # которое выбирает пользователь с списке листов в текущем файле.
            self.ui.box_sheet_1.currentTextChanged.connect(
                lambda val=self.get_select_element("box_sheet_1"): self.file.get_active_sheet(val)
            )
            print(f'{self.file.active_sheet=}\n'
                  f'{self.file.sheets_list=}\n')

    def save_input_data(self, input_list: list):
        data_key: str = self.ui.box_point_1.currentText()
        ok, err = self.file.save_in_file(key=data_key, data=input_list)
        if not ok:
            return err

    def get_select_element(self, tag_name):
        return self.ui.__dict__[tag_name].currentText()

    # Демонстрация текста ошибки в окне
    def show_error_text(self, error):
        self.clear_message()

        # Выводим текст об ошибке и меняем его цвет
        self.ui.label_error.setText(error["text"])
        self.ui.label_error.adjustSize()
        self.ui.label_error.setStyleSheet(f'color: {error["color"]};')

    # TODO: так, в дальнейшем можно объеденить в одну функцию
    # через передачу доп.параметра в self.ui.__dict__["param"] ...
    def show_status_text(self, status):
        self.clear_message()

        self.ui.label_status.setText(status["text"])
        self.ui.label_status.adjustSize()
        self.ui.label_status.setStyleSheet(f'color: {status["color"]};')

    def clear_message(self):
        self.ui.label_status.setText("")
        self.ui.label_error.setText("")


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    try:
        main()  # то запускаем функцию main()
    except KeyboardInterrupt:
        print("Окно закрыто")
