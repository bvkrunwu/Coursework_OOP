from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class AbstractAPIConnector(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получение вакансий по ключевому слову"""
        pass


class HeadHunterAPI(AbstractAPIConnector):
    """Конкретная реализация для работы с hh.ru"""

    def __init__(self):
        """
        Инициализирует экземпляр класса HeadHunterAPI.

        Устанавливает базовые настройки для работы с API HeadHunter, включая базовый URL и заголовки User-Agent.
        """
        self.__base_url: str = "https://api.hh.ru/"
        self.__headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}

    def connect(self) -> None:
        """Приватный метод подключения к API"""
        response = requests.get(self.__base_url)
        response.raise_for_status()

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получение вакансий по ключевому слову"""
        self.connect()
        endpoint: str = f"{self.__base_url}vacancies"
        params: Dict[str, Any] = {"text": keyword, "per_page": 100}
        response = requests.get(endpoint, headers=self.__headers, params=params)
        response.raise_for_status()
        return response.json()["items"]
