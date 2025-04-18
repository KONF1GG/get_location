# Get Location

Этот проект предназначен для получения геолокационных данных на основе адресов. Программа использует API и парсинг данных для извлечения координат и другой информации, а также сохраняет результаты в базу данных.

## Возможности

- Получение координат через Nominatim API.
- Использование Yandex Maps для получения данных, если Nominatim API не возвращает результат.
- Сохранение данных в базу данных MySQL.
- Уведомления через Telegram о ходе выполнения.

## Установка

### 1. Установите пакетный менеджер `uv`

Следуйте [официальной документации](https://docs.astral.sh/uv/getting-started/installation/) для установки `uv`.

### 2. Установите зависимости

Выполните следующую команду для установки всех необходимых зависимостей:

```bash
uv sync
```

Эта команда установит зависимости, указанные в файле `pyproject.toml`.

### 3. Настройте файл `.env`

Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:

```
BD_AUTHORIZATION=<ваш_токен>
MYSQL_USER=<пользователь_базы_данных>
MYSQL_PASSWORD=<пароль_базы_данных>
MYSQL_HOST=<хост_базы_данных>
MYSQL_PORT=<порт_базы_данных>
MYSQL_DB=<имя_базы_данных>
TOKEN_TELEGRAM=<телеграм_токен>
CHAT_ID=<ваш_id_чата>
```

### 4. Настройте Telegram уведомления

Если уведомления Telegram не нужны, закомментируйте вызовы функции `send_telegram_message` в коде и замените её на пустую функцию, например:

```python
def send_telegram_message(message):
    pass
```

## Запуск

Для запуска программы выполните следующую команду:

```bash
uv run mainScript
```

## Структура проекта

- `mainScript.py` — основной скрипт для выполнения программы.
- `data.py` — файл для работы с конфигурацией и переменными окружения.
- `notification_telegram.py` — модуль для отправки уведомлений в Telegram.
- `pyproject.toml` — файл с зависимостями проекта.
- `README.md` — документация проекта.
