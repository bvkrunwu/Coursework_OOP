import pytest

from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    parse_salary_range,
    print_vacancies,
    sort_vacancies,
)
from src.vacancy import Vacancy


# Создание фикстуры с тестовыми вакансиями
@pytest.fixture
def sample_vacancies():
    return [
        Vacancy(
            "Разработчик Python",
            "https://example.com/1",
            100000,
            "Требуется разработчик Python.",
            "Нет опыта",
            "Полная занятость",
            "Полный день",
        ),
        Vacancy(
            "JavaScript Developer",
            "https://example.com/2",
            80000,
            "Опыт работы с JavaScript.",
            "Средний уровень",
            "Полная занятость",
            "Полный день",
        ),
        Vacancy(
            "Frontend Engineer",
            "https://example.com/3",
            90000,
            "Опыт работы с React и Vue.js.",
            "Средний уровень",
            "Полная занятость",
            "Полный день",
        ),
        Vacancy(
            "Backend Developer",
            "https://example.com/4",
            120000,
            "Опыт работы с Django и Flask.",
            "Высокий уровень",
            "Полная занятость",
            "Полный день",
        ),
        Vacancy(
            "DevOps Specialist",
            "https://example.com/5",
            110000,
            "Опыт работы с Docker и Kubernetes.",
            "Высокий уровень",
            "Полная занятость",
            "Полный день",
        ),
    ]


# Тестирование функции filter_vacancies
def test_filter_vacancies(sample_vacancies):
    keywords = ["Python", "Django"]
    filtered = filter_vacancies(sample_vacancies, keywords)
    assert len(filtered) == 2
    titles = [v.title for v in filtered]
    assert "Разработчик Python" in titles
    assert "Backend Developer" in titles


# Тестирование функции parse_salary_range
def test_parse_salary_range():
    range_str = "50000 - 100000"
    min_salary, max_salary = parse_salary_range(range_str)
    assert min_salary == 50000
    assert max_salary == 100000

    single_value = "80000"
    min_salary_single, max_salary_single = parse_salary_range(single_value)
    assert min_salary_single == 80000
    assert max_salary_single == 80000


# Тестирование функции get_vacancies_by_salary
def test_get_vacancies_by_salary(sample_vacancies):
    salary_range = "80000 - 110000"
    suitable_vacancies = get_vacancies_by_salary(sample_vacancies, salary_range)
    assert len(suitable_vacancies) == 4  # Исправлено с 3 на 4
    salaries = [v.salary for v in suitable_vacancies]
    assert 80000 in salaries
    assert 90000 in salaries
    assert 100000 in salaries
    assert 110000 in salaries


# Тестирование функции sort_vacancies
def test_sort_vacancies(sample_vacancies):
    sorted_vacancies = sort_vacancies(sample_vacancies)
    salaries = [v.salary for v in sorted_vacancies]
    assert salaries == [120000, 110000, 100000, 90000, 80000]


# Тестирование функции get_top_vacancies
def test_get_top_vacancies(sample_vacancies):
    top_vacancies = get_top_vacancies(sort_vacancies(sample_vacancies), 3)
    assert len(top_vacancies) == 3
    titles = [v.title for v in top_vacancies]
    assert "Backend Developer" in titles
    assert "DevOps Specialist" in titles
    assert "Разработчик Python" in titles


# Тестирование функции print_vacancies
def test_print_vacancies(capfd, sample_vacancies):
    print_vacancies(sample_vacancies)
    captured = capfd.readouterr()
    output = captured.out
    assert "Разработчик Python" in output
    assert "JavaScript Developer" in output
    assert "Frontend Engineer" in output
    assert "Backend Developer" in output
    assert "DevOps Specialist" in output


# Дополнительный тест для проверки краевого случая (одиночное значение зарплаты)
def test_get_vacancies_by_salary_edge_case(sample_vacancies):
    salary_range = "110000 - 110000"
    suitable_vacancies = get_vacancies_by_salary(sample_vacancies, salary_range)
    assert len(suitable_vacancies) == 1
    assert suitable_vacancies[0].salary == 110000
