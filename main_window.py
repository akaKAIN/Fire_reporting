import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from py_windows.design import Ui_MainWindow
import saver
import json
import os


from PyQt5.QtWidgets import QComboBox

DATA = {}  # Загружается из json-файла при инициализации класса ExampleApp
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
    "no_file": {
        "text": "Не найден Excel-файл.",
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
        "color": "green"
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

    # TODO: подключение Excel-файла для дальнейшей работы. Проверка файла валидность.
    def select_file(self, file_name):
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

    # Функция нициализации выпадающего списка файлов и связывание с выпадающим списком листов в документе
    def load_files_list(self):
        files_list = self.file.get_files_list()
        files_list.insert(0, "-")

        # Составление выпадающего списка файлов
        self.ui.box_file_1.addItems(files_list)

        # Добавление сигнала в поле списка файлов. Через lambda реализована передача параметра с именем,
        # которое выбирает пользователь с списке файлов в текущей директории
        self.ui.box_file_1.currentTextChanged.connect(
            lambda val=self.get_select_element("box_file_1"): self.file.get_sheets_list(val)
        )
        # TODO: вставить список листов из файла (пока не реализовано)

        self.ui.box_sheet_1.clear()
        sheets_list, error = self.file.get_sheets_list(self.file.file_name)
        self.ui.box_sheet_1.addItem("-")
        if error:
            self.show_error_text(error)
        else:
            self.ui.box_sheet_1.addItems(sheets_list)

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
