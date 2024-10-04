import os

import pytest
import requests_mock
from prefect.testing.utilities import prefect_test_harness

from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def environ():
    return {
        'API_URL': os.getenv('API_URL'),
        'BOT_TOKEN': os.getenv('BOT_TOKEN'),
        'CHAT_ID': os.getenv('CHAT_ID'),
    }


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as mocker:
        yield mocker


@pytest.fixture
def mock_telegram_api():
    with requests_mock.Mocker() as mocker:
        yield mocker


@pytest.fixture
def prefect_environment():
    with prefect_test_harness():
        yield
