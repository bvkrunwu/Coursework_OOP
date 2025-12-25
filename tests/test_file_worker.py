import pytest

from src.file_worker import AbstractFileHandler, CSVFileHandler, ExcelFileHandler, JSONFileHandler, TextFileHandler


@pytest.fixture(scope="function")
def temp_json_file(tmp_path):
    file_path = tmp_path / "test_vacancies.json"
    yield file_path
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def temp_csv_file(tmp_path):
    file_path = tmp_path / "test_vacancies.csv"
    yield file_path
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="function")
def temp_txt_file(tmp_path):
    file_path = tmp_path / "test_vacancies.txt"
    yield file_path
    file_path.unlink(missing_ok=True)


# Тесты для AbstractFileHandler
def test_abstract_class():
    assert hasattr(AbstractFileHandler, "load_data")
    assert hasattr(AbstractFileHandler, "append_data")
    assert hasattr(AbstractFileHandler, "remove_data")
    assert hasattr(AbstractFileHandler, "db_connect")
    assert hasattr(AbstractFileHandler, "db_insert")
    assert hasattr(AbstractFileHandler, "db_select")


# Тесты для JSONFileHandler
def test_json_load_data(temp_json_file):
    handler = JSONFileHandler(str(temp_json_file))
    temp_json_file.write_text("[]")
    data = handler.load_data()
    assert data == []


def test_json_append_data(temp_json_file):
    handler = JSONFileHandler(str(temp_json_file))
    data = [{"key": "value"}]
    handler.append_data(data)
    loaded_data = handler.load_data()
    assert loaded_data == data


def test_json_remove_data(temp_json_file):
    handler = JSONFileHandler(str(temp_json_file))
    initial_data = [{"key": "value"}, {"other_key": "other_value"}]
    handler.append_data(initial_data)
    handler.remove_data([initial_data[0]])
    remaining_data = handler.load_data()
    assert remaining_data == [initial_data[1]]


# Тесты для CSVFileHandler
def test_csv_load_data(temp_csv_file):
    handler = CSVFileHandler(str(temp_csv_file))
    temp_csv_file.write_text("key,value\nfirst,second")
    data = handler.load_data()
    assert data == [{"key": "first", "value": "second"}]


def test_csv_append_data(temp_csv_file):
    handler = CSVFileHandler(str(temp_csv_file))
    data = [{"key": "value"}]
    handler.append_data(data)
    loaded_data = handler.load_data()
    assert loaded_data == data


# Тесты для TextFileHandler
def test_text_load_data(temp_txt_file):
    handler = TextFileHandler(str(temp_txt_file))
    temp_txt_file.write_text("Line 1\nLine 2")
    data = handler.load_data()
    assert data == ["Line 1\n", "Line 2"]


# Тесты для ExcelFileHandler (проверка заглушек)
def test_excel_db_methods():
    handler = ExcelFileHandler()
    handler.db_connect()
    handler.db_insert([])
    selected_data = handler.db_select("")
    assert selected_data == []
