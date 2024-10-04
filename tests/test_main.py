import pytest
import pandas as pd
from main import load_csv, call_api, process_data, save_to_json, send_telegram_notification, my_parallel_flow


def test_load_csv(tmp_path):
    test_csv = tmp_path / "test.csv"
    df = pd.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
    df.to_csv(test_csv, index=False)
    result = load_csv(test_csv)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ['id', 'value']


def test_call_api(mock_api, environ):
    mock_api.get(f"{environ.get('API_URL')}?id=1", json={"id": 1, "name": "Test"})
    result = call_api({'id': 1})
    assert result == {"id": 1, "name": "Test"}


def test_process_data():
    api_data = [{"id": 1, "name": "Test1"}, {"id": 2, "name": "Test2"}]
    result = process_data(api_data)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ['id', 'name']


def test_save_to_json(tmp_path):
    processed_data = pd.DataFrame({"id": [1, 2], "name": ["Test1", "Test2"]})
    output_file = tmp_path / "output.json"
    save_to_json(processed_data, output_file)
    assert output_file.exists()
    df_loaded = pd.read_json(output_file)
    assert list(df_loaded.columns) == ["id", "name"]
    assert len(df_loaded) == 2


def test_send_telegram_notification(mock_telegram_api, environ):
    mock_telegram_api.post(f"https://api.telegram.org/bot{environ.get('BOT_TOKEN')}/sendMessage", status_code=200)
    send_telegram_notification("Test message")
    assert mock_telegram_api.called
    assert mock_telegram_api.call_count == 1


@pytest.mark.parametrize("test_data, api_responses", [([{'id': 1}, {'id': 2}], [{'id': 1, 'name': 'Test1'}, {'id': 2, 'name': 'Test2'}])])
def test_full_flow(mock_api, mock_telegram_api, tmp_path, test_data, api_responses, prefect_environment, environ):
    for idx, row in enumerate(test_data):
        mock_api.get(f"{environ.get('API_URL')}?id={row['id']}", json=api_responses[idx])
    mock_telegram_api.post(f"https://api.telegram.org/bot{environ.get('BOT_TOKEN')}/sendMessage", status_code=200)
    test_csv = tmp_path / "test.csv"
    pd.DataFrame(test_data).to_csv(test_csv, index=False)
    output_file = tmp_path / "output.json"
    my_parallel_flow(file_path=test_csv, output_path=output_file)
    assert output_file.exists()
    df_loaded = pd.read_json(output_file)
    assert list(df_loaded.columns) == ["id", "name"]
    assert len(df_loaded) == len(test_data)
    assert mock_telegram_api.called
    assert mock_telegram_api.call_count == 1
