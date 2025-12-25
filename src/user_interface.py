from src.file_worker import JSONFileHandler
from src.hh_api import HeadHunterAPI
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy


def user_interaction():
    """Основная функция для взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    json_handler = JSONFileHandler()

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    # Получение вакансий
    raw_vacancies = hh_api.get_vacancies(search_query)
    print(f"Всего найдено вакансий: {len(raw_vacancies)}")

    vacancies = [
        Vacancy(
            v["name"],
            v["alternate_url"],
            v["salary"]["to"] if v["salary"] else 0,
            v["snippet"]["responsibility"],
            v.get("experience", {}).get("name"),  # Опыт работы
            v.get("employment", {}).get("name"),  # Тип занятости
            v.get("schedule", {}).get("name"),  # График работы
        )
        for v in raw_vacancies
    ]

    # Фильтрация и сортировка вакансий
    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    print(f"Вакансий после фильтрации ключевыми словами: {len(filtered_vacancies)}")

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    print(f"Вакансий после фильтрации по зарплате: {len(ranged_vacancies)}")

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    print(f"Вакансий после сортировки: {len(sorted_vacancies)}")

    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print(f"Конечный список вакансий (топ-{top_n}): {len(top_vacancies)}")

    # Сохранение и вывод результатов
    json_handler.append_data([v.to_dict() for v in top_vacancies])
    print_vacancies(top_vacancies)
