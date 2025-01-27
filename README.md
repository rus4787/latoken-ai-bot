# README.md

## Telegram-бот AI для оценки кандидатов в Латокен

### Обзор

Этот Telegram-бот AI предназначен для помощи кандидатам, которые рассматривают возможность работы в Latoken, предоставляя информацию о компании, хакатоне, культуре и проводя тесты для оценки их понимания. Бот построен с использованием Python и интегрирует Telegram Bot API и OpenAI для интерактивных ответов.

### Предварительные требования

- Python 3.12 или выше
- Библиотеки Python:
  - `python-telegram-bot`
  - `openai`
- Установленное приложение Telegram на вашем устройстве
- API-ключи для Telegram бота и OpenAI

### Установка

1. **Клонирование репозитория**

   ```bash
   git clone https://github.com/rus4787/latoken-ai-bot.git
   cd latoken-ai-bot
   ```

2. **Установка зависимостей**

   ```bash
   pip install python-telegram-bot openai
   ```

3. **Настройка конфигурационных файлов**

   - Создайте файл `config.py` для хранения ваших API-ключей:

     ```python
     token_bot = "YOUR_TELEGRAM_BOT_TOKEN"
     token_gpt = "YOUR_OPENAI_API_KEY"
     ```

4. **Проверка путей импорта**

   - Убедитесь, что все пути импорта в скриптах корректны, особенно после переименования файлов.

### Запуск бота

1. **Запуск бота локально**

   ```bash
   python flash.py
   ```

2. **Деплой бота (по желанию)**

   - Для непрерывной работы рассмотрите возможность размещения бота на платформе hosting, такой как Heroku или AWS.

### Функциональные возможности бота

#### Команды

- **/start**: Начинает диалог и отображает главное меню с кнопками для каждой команды.
- **/help**: Предоставляет список доступных команд и их описание, а также отображает меню с кнопками для каждой команды.
- **/about**: Определяет информацию о боте и его функциях.
- **/culture**: Предоставляет сведения о культуре Latoken.
- **/interview**: Описывает процесс собеседования в Latoken.
- **/hackathon**: Дает информацию о хакатоне Latoken.
- **/test**: Проводит тест для оценки понимания кандидатом культуры и процессов в Latoken.
- **/ask**: Разрешает кандидатам задавать вопросы и получать ответы от бота.

#### Функциональность тестирования

- **Подсчет уникальных вопросов**: Бот отслеживает уникальные вопросы, заданные кандидатом, и прекращает тест после того, как все уникальные вопросы из списка были заданы.
- **Выбор из нескольких вариантов**: Бот предоставляет список вопросов, из которых кандидат может выбирать.
- **Список вопросов**: При запуске теста бот выводит список доступных вопросов, чтобы кандидат мог выбрать один из них.
- **Рандомные ответы**: Для каждого вопроса бот выбирает случайный ответ из предопределенных вариантов.

### Устранение неполадок

- **Ошибки импорта**: Убедитесь, что все имена файлов и инструкции импорта корректны. Избегайте конфликтов имен с стандартными модулями Python.
- **Проблемы с подключением к API**: Проверьте, что ваши API-ключи корректны и что у вас есть интернет-соединение.

### Будущие улучшения

- **Интерактивные тесты**: Реализовать более интерактивные и динамические функции тестирования.
- **Расширенный модуль тестирования**: Включить более широкий спектр вопросов и уровней сложности.
- **Отслеживание пользователей**: Добавить функциональность для отслеживания прогресса и результатов пользователей.

### Сильные стороны проекта

1. **Интеграция AI**: Использование OpenAI для динамических ответов.
2. **Пользовательский интерфейс**: Бот предоставляет меню с кнопками для удобства навигации.
3. **Комплексный модуль тестирования**: Оценивает понимание кандидатов через серию вопросов с учетом уникальных вопросов и рандомных ответов.
4. **Модульная структура кода**: Разделение обязанностей с помощью различных файлов для конфигурации, описаний и ответов.
5. **Масштабируемость**: Легко расширяемый с добавлением дополнительных функций или команд.
6. **Ясная документация**: README предоставляет пошаговое руководство, что полезно для новых участников.

### Контакт

Для любых вопросов или отзывов свяжитесь с командой разработки по адресу [habibulin.1987.2013@gmail.com]

