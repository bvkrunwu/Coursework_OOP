import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Generic, List, TypeVar

TData = TypeVar("TData")


class AbstractFileHandler(Generic[TData], ABC):
    """
    Абстрактный класс для работы с файлами.

    Определяет общие методы для работы с файлами различных форматов.
    """

    @abstractmethod
    def load_data(self) -> TData:
        """
        Загрузка данных из файла.

        :return: Загруженные данные определенного типа TData
        """
        pass

    @abstractmethod
    def append_data(self, data: TData) -> None:
        """
        Добавление данных в файл.

        :param data: Данные для добавления
        """
        pass

    @abstractmethod
    def remove_data(self, data: TData) -> None:
        """
        Удаление данных из файла.

        :param data: Данные для удаления
        """
        pass

    @abstractmethod
    def db_connect(self) -> None:
        """
        Заглушка для подключения к базе данных.
        """
        pass

    @abstractmethod
    def db_insert(self, data: TData) -> None:
        """
        Заглушка для вставки данных в базу данных.

        :param data: Данные для вставки
        """
        pass

    @abstractmethod
    def db_select(self, query: str) -> List[TData]:
        """
        Заглушка для выборки данных из базы данных.

        :param query: SQL-запрос
        :return: Список выбранных данных
        """
        pass


class JSONFileHandler(AbstractFileHandler[List[Dict[str, str]]]):
    """
    Реализация для работы с JSON-файлами.
    """

    def __init__(self, filename: str = "data/vacancies.json"):
        self.__filename: str = filename
        self.__full_path: Path = Path.cwd() / self.__filename
        self.__full_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> List[Dict[str, str]]:
        """
        Загрузка данных из JSON-файла.

        :return: Список словарей с данными
        """
        if self.__full_path.exists():
            with open(self.__full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def append_data(self, data: List[Dict[str, str]]) -> None:
        """
        Добавление данных в JSON-файл.

        :param data: Список словарей с данными для добавления
        """
        existing_data = self.load_data()
        new_data = [item for item in data if item not in existing_data]
        combined_data = existing_data + new_data
        with open(self.__full_path, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)

    def remove_data(self, data: List[Dict[str, str]]) -> None:
        """
        Удаление данных из JSON-файла.

        :param data: Список словарей с данными для удаления
        """
        existing_data = self.load_data()
        updated_data = [item for item in existing_data if item not in data]
        with open(self.__full_path, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4, ensure_ascii=False)

    def db_connect(self) -> None:
        """
        Заглушка для подключения к базе данных.
        """
        print("Подключение к базе данных не поддерживается для JSON-файлов.")

    def db_insert(self, data: List[Dict[str, str]]) -> None:
        """
        Заглушка для вставки данных в базу данных.

        :param data: Список словарей с данными для вставки
        """
        print("Вставка данных в базу данных не поддерживается для JSON-файлов.")

    def db_select(self, query: str) -> List[Dict[str, str]]:
        """
        Заглушка для выборки данных из базы данных.

        :param query: SQL-запрос
        :return: Список словарей с выбранными данными
        """
        print("Выборка данных из базы данных не поддерживается для JSON-файлов.")
        return []


class CSVFileHandler(AbstractFileHandler[List[Dict[str, str]]]):
    """
    Конкретная реализация для работы с CSV-файлами.
    """

    def __init__(self, filename: str = "data/vacancies.csv"):
        self.__filename: str = filename
        self.__full_path: Path = Path.cwd() / self.__filename
        self.__full_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> List[Dict[str, str]]:
        """
        Загрузка данных из CSV-файла.

        :return: Список словарей с данными
        """
        if self.__full_path.exists():
            with open(self.__full_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return list(reader)
        return []

    def append_data(self, data: List[Dict[str, str]]) -> None:
        """
        Добавление данных в CSV-файл.

        :param data: Список словарей с данными для добавления
        """
        existing_data = self.load_data()
        fieldnames = data[0].keys() if data else []
        new_data = [item for item in data if item not in existing_data]
        combined_data = existing_data + new_data
        with open(self.__full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_data)

    def remove_data(self, data: List[Dict[str, str]]) -> None:
        """
        Удаление данных из CSV-файла.

        :param data: Список словарей с данными для удаления
        """
        existing_data = self.load_data()
        updated_data = [item for item in existing_data if item not in data]
        fieldnames = updated_data[0].keys() if updated_data else []
        with open(self.__full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)

    def db_connect(self) -> None:
        """
        Заглушка для подключения к базе данных.
        """
        print("Подключение к базе данных не поддерживается для CSV-файлов.")

    def db_insert(self, data: List[Dict[str, str]]) -> None:
        """
        Заглушка для вставки данных в базу данных.

        :param data: Список словарей с данными для вставки
        """
        print("Вставка данных в базу данных не поддерживается для CSV-файлов.")

    def db_select(self, query: str) -> List[Dict[str, str]]:
        """
        Заглушка для выборки данных из базы данных.

        :param query: SQL-запрос
        :return: Список словарей с выбранными данными
        """
        print("Выборка данных из базы данных не поддерживается для CSV-файлов.")
        return []


class TextFileHandler(AbstractFileHandler[List[str]]):
    """
    Конкретная реализация для работы с TXT-файлами.
    """

    def __init__(self, filename: str = "data/vacancies.txt"):
        self.__filename: str = filename
        self.__full_path: Path = Path.cwd() / self.__filename
        self.__full_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> List[str]:
        """
        Загрузка данных из TXT-файла.

        :return: Список строк с данными
        """
        if self.__full_path.exists():
            with open(self.__full_path, "r", encoding="utf-8") as f:
                return f.readlines()
        return []

    def append_data(self, data: List[str]) -> None:
        """
        Добавление данных в TXT-файл.

        :param data: Список строк с данными для добавления
        """
        with open(self.__full_path, "a", encoding="utf-8") as f:
            for item in data:
                f.write(str(item) + "\n")

    def remove_data(self, data: List[str]) -> None:
        """
        Удаление данных из TXT-файла.

        :param data: Список строк с данными для удаления
        """
        existing_data = self.load_data()
        updated_data = [line for line in existing_data if line.strip() not in data]
        with open(self.__full_path, "w", encoding="utf-8") as f:
            f.writelines(updated_data)

    def db_connect(self) -> None:
        """
        Заглушка для подключения к базе данных.
        """
        print("Подключение к базе данных не поддерживается для TXT-файлов.")

    def db_insert(self, data: List[str]) -> None:
        """
        Заглушка для вставки данных в базу данных.

        :param data: Список строк с данными для вставки
        """
        print("Вставка данных в базу данных не поддерживается для TXT-файлов.")

    def db_select(self, query: str) -> List[str]:
        """
        Заглушка для выборки данных из базы данных.

        :param query: SQL-запрос
        :return: Список строк с выбранными данными
        """
        print("Выборка данных из базы данных не поддерживается для TXT-файлов.")
        return []


class ExcelFileHandler(AbstractFileHandler[List[Dict[str, str]]]):
    """
    Заготовка для работы с Excel-файлами.
    """

    def __init__(self, filename: str = "data/vacancies.xlsx"):
        self.__filename: str = filename
        self.__full_path: Path = Path.cwd() / self.__filename
        self.__full_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> List[Dict[str, str]]:
        """
        Заглушка для загрузки данных из Excel-файла.

        :return: Список словарей с данными
        """
        print("Работа с Excel-файлами не реализована.")
        return []

    def append_data(self, data: List[Dict[str, str]]) -> None:
        """
        Заглушка для добавления данных в Excel-файл.

        :param data: Список словарей с данными для добавления
        """
        print("Работа с Excel-файлами не реализована.")

    def remove_data(self, data: List[Dict[str, str]]) -> None:
        """
        Заглушка для удаления данных из Excel-файла.

        :param data: Список словарей с данными для удаления
        """
        print("Работа с Excel-файлами не реализована.")

    def db_connect(self) -> None:
        """
        Заглушка для подключения к базе данных.
        """
        print("Подключение к базе данных не поддерживается для Excel-файлов.")

    def db_insert(self, data: List[Dict[str, str]]) -> None:
        """
        Заглушка для вставки данных в базу данных.

        :param data: Список словарей с данными для вставки
        """
        print("Вставка данных в базу данных не поддерживается для Excel-файлов.")

    def db_select(self, query: str) -> List[Dict[str, str]]:
        """
        Заглушка для выборки данных из базы данных.

        :param query: SQL-запрос
        :return: Список словарей с выбранными данными
        """
        print("Выборка данных из базы данных не поддерживается для Excel-файлов.")
        return []
