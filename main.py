import os
import pandas as pd
import prefect
import requests
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


@prefect.task
def load_csv(file_path):
    data = pd.read_csv(file_path)
    return data


@prefect.task(retries=3, retry_delay_seconds=10)
def call_api(row):
    try:
        response = requests.get(f"{API_URL}?id={row['id']}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger = prefect.get_run_logger()
        logger.error(f"API call failed for row {row['id']}: {e}")
        raise


@prefect.task
def process_data(api_data):
    df = pd.DataFrame(api_data)
    return df


@prefect.task
def save_to_json(processed_data, output_path):
    processed_data.to_json(output_path, orient='records')


@prefect.task
def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        logger = prefect.get_run_logger()
        logger.error("Failed to send Telegram notification")


@prefect.flow
def my_parallel_flow(file_path, output_path):
    logger = prefect.get_run_logger()
    logger.info("Starting data processing")

    data = load_csv(file_path)

    processed_data = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(call_api, row) for _, row in data.iterrows()]
        for future in futures:
            api_data = future.result()
            processed_row = process_data(api_data)
            processed_data.append(processed_row)

    save_to_json(pd.DataFrame(processed_data), output_path)
    send_telegram_notification("Data processing flow completed successfully.")
    logger.info("Data processing flow finished")
