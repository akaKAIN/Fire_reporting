import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from py_windows.design import Ui_MainWindow
import os
import json

from PyQt5.QtWidgets import QComboBox


DATA = []  # Загружается из json-файла при инициализации класса ExampleApp
JSON_FILE = 'name_list.json'
INPUT_FIELD_TYPE = QtWidgets.QLineEdit



ERRORS = {
    "not_number": {
        "text": "Ошибка ввода данных - буквы в числовом поле",
        "color": "red"
        },

    "no_name_list": {
        "text": "Не найден файл со списками Почарных Частей",
        "color": "red"
        },
}

STATUS = {
    "no_excel_file": {
        "text": "Выберете файл для начала работы",
        "color": "orange"
        },
    "excel_file_select": {
        "text": "Файл успешно выбран",
        "color": "orange"
        },
    "is_valid": {
        "text": "Данные успешно сохранены",
        "color": "darkgreen"
        },
    "is_empty": {
        "text": "Форма пуста. Введите данные для сохранения их в файл.",
        "color": "darkgoldenrod"
        },

}


class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.ui.pushButton.clicked.connect(self.print_fields)                 # Кнопка вывода в консоль имен полей
        self.ui.pushButton_2.clicked.connect(self.get_data_from_fields)       # Кнопка проверки данных (+save +clear)
        self.ui.pushButton_3.clicked.connect(self.clear_fields)
        self.load_name_list(JSON_FILE)                                        # Инициализация выпадающего списка зон
        self.clear_fields()
#         self.ui.box_area_1.clicked.connect(self.clear_fields)

    # Загрузка данных о Пожарных частях в районах
    def load_name_list(self, file_name):
        self.ui.box_area_1.addItem("-")           # Добавление первого (пустого) значения в выпадающий список
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                DATA = json.loads(f.read())
            for area in DATA:
                self.ui.box_area_1.addItems(area.keys())

        else:
            self.show_error_text(ERRORS["no_name_list"])

    # TODO: подключение Excel-файла для дальнейшей работы. Проверка файла валидность.
    def select_file(file_name):
        pass

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
            # TODO: передавать данные в Excel-file для сохранения
            self.clear_fields()
            self.show_status_text(STATUS['is_valid'])
            print(data)

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
