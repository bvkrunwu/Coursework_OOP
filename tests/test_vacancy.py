import pytest

from src.vacancy import Vacancy


# Тестирование инициализации объекта Vacancy
def test_vacancy_initialization():
    """
    Проверяет корректность инициализации объекта Vacancy.
    """
    vacancy = Vacancy(
        title="Разработчик Python",
        link="https://example.com/1",
        salary="100000",
        description="<strong>Требуется разработчик Python.</strong>",
        experience="Нет опыта",
        employment="Полная занятость",
        schedule="Полный день",
    )

    assert vacancy.title == "Разработчик Python"
    assert vacancy.link == "https://example.com/1"
    assert vacancy.salary == 100000
    assert vacancy.description == "Требуется разработчик Python."
    assert vacancy.experience == "Нет опыта"
    assert vacancy.employment == "Полная занятость"
    assert vacancy.schedule == "Полный день"


# Тестирование метода to_dict
def test_vacancy_to_dict():
    """
    Проверяет корректность преобразования объекта Vacancy в словарь.
    """
    vacancy = Vacancy(
        title="Разработчик Python",
        link="https://example.com/1",
        salary="100000",
        description="<strong>Требуется разработчик Python.</strong>",
    )

    vacancy_dict = vacancy.to_dict()
    assert vacancy_dict == {
        "title": "Разработчик Python",
        "link": "https://example.com/1",
        "salary": 100000,
        "description": "Требуется разработчик Python.",
        "experience": None,
        "employment": None,
        "schedule": None,
    }


# Тестирование валидации зарплаты
@pytest.mark.parametrize(
    "input_salary,expected_output",
    [
        ("100000", 100000),
        (100000, 100000),
        (100000.0, 100000),
        ("abc", 0),
        ("100k", 0),
        (-50000, 0),
        ("", 0),
        (None, 0),
        ("100.5", 0),
    ],
)
def test_validate_salary(input_salary, expected_output):
    """
    Проверяет корректность валидации зарплаты.
    """
    vacancy = Vacancy(
        title="Разработчик Python",
        link="https://example.com/1",
        salary=input_salary,
        description="Требуется разработчик Python.",
    )

    assert vacancy.salary == expected_output


# Тестирование чистки HTML-тегов
@pytest.mark.parametrize(
    "input_description,expected_output",
    [
        ("<strong>Требуется разработчик Python.</strong>", "Требуется разработчик Python."),
        ("<div><p>Описание вакансии.</p></div>", "Описание вакансии."),
        ("<span>Опыт работы:</span> 5 лет", "Опыт работы: 5 лет"),
        ("<invalid-tag>Некорректный тег.</invalid-tag>", "Некорректный тег."),
        ("Простой текст без тегов", "Простой текст без тегов"),
        ("", ""),
        (None, "Без описания"),
    ],
)
def test_clean_html(input_description, expected_output):
    """
    Проверяет корректность чистки HTML-тегов из описания.
    """
    vacancy = Vacancy(
        title="Разработчик Python", link="https://example.com/1", salary="100000", description=input_description
    )

    assert vacancy.description == expected_output


# Тестирование операторов сравнения
def test_comparison_operators():
    """
    Проверяет корректность работы операторов сравнения вакансий.
    """
    vacancy1 = Vacancy(
        title="Разработчик Python",
        link="https://example.com/1",
        salary="100000",
        description="Требуется разработчик Python.",
    )

    vacancy2 = Vacancy(
        title="JavaScript Developer",
        link="https://example.com/2",
        salary="80000",
        description="Опыт работы с JavaScript.",
    )

    vacancy3 = Vacancy(
        title="Frontend Engineer",
        link="https://example.com/3",
        salary="90000",
        description="Опыт работы с React и Vue.js.",
    )

    assert vacancy1 > vacancy2
    assert vacancy1 >= vacancy3
    assert vacancy2 < vacancy3
    assert vacancy2 <= vacancy3
    assert vacancy1 != vacancy2
    assert vacancy1 == vacancy1
