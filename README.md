# CSV и API Processing Flow с использованием Prefect 3.0

## Описание
Этот проект выполняет обработку данных из CSV-файла, запрашивает данные с внешнего API для каждой строки, обрабатывает их с использованием Pandas и сохраняет результат в JSON-файле. Проект построен с использованием **Prefect 3.0** для управления задачами, а также поддерживает Docker и автоматическое масштабирование worker'ов.

Основные возможности:
- Обработка данных из CSV.
- Вызов сторонних API.
- Сохранение результата в JSON.
- Отправка уведомлений в Telegram о завершении работы.
- Поддержка лимитов на параллельные задачи, частоту выполнения и повторные попытки.
- Легкий мониторинг и управление задачами через **Prefect Orion**.

## Стек технологий

- **Prefect 3.0**
- **Pandas** для обработки данных.
- **Requests** для вызова внешних API.
- **Docker** для контейнеризации.
- **Docker Compose** для оркестрации.
- **Prefect Orion UI** для мониторинга.

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/pyfullstackdev/testproject-prefect.git
cd testproject-prefect
```

### 2. Установка зависимостей

Все зависимости указаны в файле requirements.txt. Вы можете установить их вручную или с помощью Docker.

> Ручная установка (локально)
Если хотите запустить проект локально, создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Установка с помощью Docker
Если вы предпочитаете использовать Docker, следуйте следующей инструкции.

## Использование Docker
### 1. Сборка и запуск контейнеров
Для автоматизации запуска всех компонентов проекта используется Docker Compose. Для этого нужно собрать и запустить контейнеры:

```bash
docker-compose up --build
```

### Контейнеры включают:
* Prefect Orion UI для мониторинга задач.
* Prefect worker для выполнения задач.

### 2. Открытие Prefect UI
После запуска контейнеров вы можете открыть Prefect Orion UI, чтобы отслеживать выполнение задач и их статус:

http://localhost:4200

### 3. Регистрация и запуск flow
После того как контейнеры запущены, вам нужно зарегистрировать flow с помощью Prefect CLI:

```bash
prefect deployment build -n csv-processing --apply main.py:my_parallel_flow
```

Это создаст deployment для вашего flow. Flow будет автоматически выполняться на основе расписания, указанного в prefect.yml.

Структура проекта
```text
├── Dockerfile                # Описание Docker образа для worker'ов
├── docker-compose.yml        # Описание контейнеров для docker-compose
├── my_flow.py                # Основной код Prefect flow
├── prefect.yml               # Конфигурация Prefect flow и worker'ов
├── requirements.txt          # Зависимости проекта
├── README.md                 # Документация проекта
├── tests/
│   ├── conftest.py           # Общие фикстуры для тестов
│   ├── test_my_flow.py       # Тесты для проекта с использованием pytest
├── data/
│   ├── input.csv             # Пример CSV файла с данными для обработки
│   ├── output.json           # Файл для сохранения результатов
```

### Flow
Основной поток задач **my_parallel_flow** выполняет следующие шаги:

#### 1. Загрузка данных из CSV:
* Чтение данных из файла CSV.
#### 2. Запрос данных с внешнего API:
* Для каждой строки CSV выполняется запрос к внешнему API.
#### 3. Обработка данных:
* Данные, полученные из API, обрабатываются с использованием Pandas.
#### 4. Сохранение данных в JSON:
* Результаты сохраняются в JSON-файл.
#### 5. Отправка уведомления в Telegram:
* После завершения процесса отправляется уведомление в указанный чат Telegram.

## Настройки
Telegram уведомления
Для отправки уведомлений в Telegram, добавьте свой Telegram token и chat ID в переменные окружения.

Пример:
```bash
API_URL=https://api.example.com/data
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

## Тестирование
Для тестирования проекта используется pytest. Тесты покрывают отдельные функции и полный flow. Для мока внешних API используется requests_mock.

Запуск тестов:
```bash
pytest
```

## Конфигурация Prefect
### 1. Лимиты
В **prefect.yml** указаны следующие лимиты:
* Concurrency Limit: Не более 5 параллельных задач.
* Rate Limit: Не более 2 запросов в минуту.
* Retries: Повторные попытки задач до 3 раз с задержкой в 10 секунд.

### 2. Расписание
Flow настроен на выполнение каждые 1 час (см. секцию **schedule** в **prefect.yml**).

## Мониторинг
Мониторинг всех задач осуществляется через Prefect Orion UI, доступный по адресу http://localhost:4200. Orion UI позволяет отслеживать состояние задач, их выполнение, ошибки и повторные попытки.

## Дополнительные настройки
Docker ограничения
Ограничения на ресурсы (CPU, память) могут быть настроены в **docker-compose.yml** для worker'ов.

Пример:

```yaml
services:
  worker:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
```

## Развертывание
Для развертывания проекта на сервере используйте Docker Compose и Prefect Orion для автоматизации процесса выполнения задач.
