import re
from typing import Dict, Optional, Union


class Vacancy:
    """
    Класс для работы с отдельными вакансиями.

    Представляет собой модель вакансии с основными характеристиками:
    - title (название вакансии),
    - link (ссылка на вакансию),
    - salary (заработная плата),
    - description (описание вакансии),
    - experience (требуемый опыт работы),
    - employment (тип занятости),
    - schedule (график работы).

    Класс поддерживает методы для преобразования объекта в словарь,
    очистки HTML-тегов из описания и валидации зарплаты.
    """

    __slots__ = ["title", "link", "salary", "description", "experience", "employment", "schedule"]

    def __init__(
        self,
        title: str,
        link: str,
        salary: Union[int, float, str],
        description: Optional[str],
        experience: Optional[str] = None,
        employment: Optional[str] = None,
        schedule: Optional[str] = None,
    ):
        """
        Инициализирует экземпляр класса Vacancy.

        :param title: Название вакансии
        :param link: Ссылка на страницу вакансии
        :param salary: Заработная плата (целое число, дробное число или строка)
        :param description: Описание вакансии (HTML-код)
        :param experience: Требуемый опыт работы
        :param employment: Тип занятости
        :param schedule: График работы
        """
        self.title = title
        self.link = link
        self.salary = self.__validate_salary(salary)
        self.description = self.__clean_html(description) if description is not None else "Без описания"
        self.experience = experience
        self.employment = employment
        self.schedule = schedule

    def to_dict(self) -> Dict[str, Optional[Union[str, int]]]:
        """
        Возвращает словарь с основными полями вакансии.

        :return: Словарь с полями вакансии
        """
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
            "experience": self.experience,
            "employment": self.employment,
            "schedule": self.schedule,
        }

    @staticmethod
    def __clean_html(text: str) -> str:
        """
        Удаляет HTML-теги из текста, включая специальные теги типа <highlighttext>.

        :param text: Входной текст с HTML-разметкой
        :return: Очищенный текст без HTML-тегов
        """
        cleaned_text = re.sub(r"<[^>]*>", "", text)
        return cleaned_text.strip()

    @staticmethod
    def __validate_salary(salary: Union[int, float, str]) -> int:
        """
        Приватный статический метод валидации зарплаты.

        Проверяет, является ли зарплата положительным числом или строкой, состоящей из цифр, и возвращает целое число.
        Если зарплата невалидная или отрицательная, возвращает 0.

        :param salary: Заработная плата (целое число, дробное число или строка)
        :return: Валидированная заработная плата в виде целого числа
        """
        if isinstance(salary, (int, float)):
            if salary > 0:
                return int(salary)
        elif isinstance(salary, str) and salary.isdigit():
            return int(salary)
        return 0

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "меньше" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии меньше, чем у другой
        """
        return self.salary < other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "больше" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии больше, чем у другой
        """
        return self.salary > other.salary

    def __eq__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "равно" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии равна зарплате другой
        """
        return self.salary == other.salary

    def __le__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "меньше или равно" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии меньше или равна зарплате другой
        """
        return self.salary <= other.salary

    def __ge__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "больше или равно" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии больше или равна зарплате другой
        """
        return self.salary >= other.salary

    def __ne__(self, other: "Vacancy") -> bool:
        """
        Определяет оператор "не равно" для сравнения вакансий по зарплате.

        :param other: Другая вакансия для сравнения
        :return: True, если зарплата текущей вакансии не равна зарплате другой
        """
        return self.salary != other.salary
