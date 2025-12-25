from unittest.mock import Mock, patch

import pytest

from src.hh_api import AbstractAPIConnector, HeadHunterAPI


# Тесты для AbstractAPIConnector
def test_abstract_class():
    """
    Проверяет наличие абстрактных методов в классе AbstractAPIConnector.
    """
    assert hasattr(AbstractAPIConnector, "connect")
    assert hasattr(AbstractAPIConnector, "get_vacancies")


# Тесты для HeadHunterAPI
def test_headhunter_init():
    """
    Проверяет корректность инициализации класса HeadHunterAPI.
    """
    api = HeadHunterAPI()
    assert api._HeadHunterAPI__base_url == "https://api.hh.ru/"
    assert api._HeadHunterAPI__headers == {"User-Agent": "HH-User-Agent"}


@patch("requests.get")
def test_headhunter_connect(mock_get):
    """
    Проверяет успешное подключение к API.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    api.connect()

    mock_get.assert_called_once_with(api._HeadHunterAPI__base_url)


@patch("requests.get")
def test_headhunter_get_vacancies_success(mock_get):
    """
    Проверяет успешное получение вакансий по ключевому слову.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"name": "Job Title"}]}
    mock_get.return_value = mock_response

    # Поддельное успешное соединение
    with patch.object(HeadHunterAPI, "connect"):
        api = HeadHunterAPI()
        result = api.get_vacancies("keyword")

        assert result == [{"name": "Job Title"}]
        mock_get.assert_called_once_with(
            "https://api.hh.ru/vacancies",
            headers={"User-Agent": "HH-User-Agent"},
            params={"text": "keyword", "per_page": 100},
        )


@patch("requests.get")
def test_headhunter_get_vacancies_failure(mock_get):
    """
    Проверяет обработку ошибки при получении вакансий.
    """
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("Not Found")
    mock_get.return_value = mock_response

    api = HeadHunterAPI()

    with pytest.raises(Exception, match="Not Found"):
        api.get_vacancies("keyword")
