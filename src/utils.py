from typing import List, Tuple

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List["Vacancy"], keywords: List[str]) -> List["Vacancy"]:
    """
    Фильтрует вакансии по наличию ключевых слов в названии или описании.

    :param vacancies: Список объектов вакансий
    :param keywords: Список ключевых слов для фильтрации
    :return: Список отфильтрованных вакансий
    """
    filtered = []
    for vacancy in vacancies:
        text = f"{vacancy.title} {vacancy.description}".lower()
        if any(keyword.lower() in text for keyword in keywords):
            filtered.append(vacancy)
    return filtered


def parse_salary_range(salary_range_str: str) -> Tuple[int, int]:
    """
    Парсит строку с диапазоном зарплат и возвращает кортеж (min_salary, max_salary).

    :param salary_range_str: Строка с диапазоном зарплат (например, "1 - 500000")
    :return: Кортеж (min_salary, max_salary)
    """
    # Удаляем лишние пробелы и символы табуляции
    clean_str = salary_range_str.strip().replace("\t", "")

    # Разбираем строку на две части по знаку "-"
    parts = clean_str.split("-")

    if len(parts) == 2:
        min_salary = int(parts[0].strip())
        max_salary = int(parts[1].strip())
    else:
        # Если диапазон задан одним числом, считаем его и минимумом, и максимумом
        single_value = int(clean_str.strip())
        min_salary = single_value
        max_salary = single_value

    return min_salary, max_salary


def get_vacancies_by_salary(vacancies: List["Vacancy"], salary_range_str: str) -> List["Vacancy"]:
    """
    Отбирает вакансии, подходящие под указанный диапазон зарплат.

    :param vacancies: Список объектов вакансий
    :param salary_range_str: Строка с диапазоном зарплат
    :return: Список вакансий, попадающих в диапазон
    """
    min_salary, max_salary = parse_salary_range(salary_range_str)
    return [v for v in vacancies if min_salary <= v.salary <= max_salary]


def sort_vacancies(vacancies: List["Vacancy"]) -> List["Vacancy"]:
    """
    Сортирует вакансии по зарплате по убыванию.

    :param vacancies: Список объектов вакансий
    :return: Отсортированный список вакансий
    """
    return sorted(vacancies, key=lambda v: v.salary, reverse=True)


def get_top_vacancies(vacancies: List["Vacancy"], count: int) -> List["Vacancy"]:
    """
    Возвращает указанное количество лучших вакансий.

    :param vacancies: Список объектов вакансий
    :param count: Количество вакансий для возврата
    :return: Список лучших вакансий
    """
    return vacancies[:count]


def print_vacancies(vacancies: List["Vacancy"]) -> None:
    """
    Печать информации о вакансиях в удобном формате.

    :param vacancies: Список объектов вакансий
    """
    for i, vacancy in enumerate(vacancies, start=1):
        print(f"\n{i}. {vacancy.title}")
        print(f"   Зарплата: {vacancy.salary}")
        print(f"   Ссылка: {vacancy.link}")
        print(f"   Описание: {vacancy.description}")
        print(f"   Опыт работы: {vacancy.experience}")
        print(f"   Тип занятости: {vacancy.employment}")
        print(f"   График работы: {vacancy.schedule}")
