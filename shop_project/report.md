---
title: Звіт до лабораторної роботи №4
permalink: /lab4/
---

# Звіт до лабораторної роботи №4

## Тема

**Назва лабораторної роботи:** Системні та інтеграційні тести. Автоматизація процесу тестування.

## Мета роботи

Навчитися перевіряти окремі компоненти програми, їхню спільну роботу та автоматично запускати тести після змін у коді.

## Виконання роботи

- створено проєкт `shop_project` із класами `Product`, `ShoppingCart`, `Inventory` та `OrderService`;
- написано unit-тести для `Product`, `ShoppingCart` і `Inventory`;
- написано інтеграційні тести, які перевіряють спільну роботу всіх чотирьох класів без використання моків;
- за допомогою `pytest-cov` визначено покриття коду тестами та створено HTML Coverage Report;
- налаштовано CI через GitHub Actions (`.github/workflows/tests.yml`) і перевірено його реакцію на успішні та помилкові тести.

## Результат

Структура проєкту:

![Структура проєкту](./screens/screen1.jpg)

Успішний запуск `pytest`:

![Запуск pytest](./screens/screen2.jpg)

Покриття з колонкою Missing (`pytest --cov=shop --cov-report=term-missing`):

![Coverage з Missing](./screens/screen3.jpg)

Головна сторінка HTML Coverage Report:

![htmlcov/index.html](./screens/screen4.jpg)

Сторінка файлу в HTML Coverage Report:

![Файл у Coverage Report](./screens/screen5.jpg)

Підсумкове покриття після додавання тестів:

![Підсумковий coverage](./screens/screen3.jpg)

Успішне виконання GitHub Actions:

![Успішний workflow](./screens/screen7.jpg)

GitHub Actions із навмисно зламаним тестом:

![Workflow з помилкою](./screens/screen8.jpg)

## Висновок

Під час виконання лабораторної роботи було написано unit- та інтеграційні тести для навчального інтернет-магазину, проаналізовано покриття коду за допомогою `pytest-cov` і HTML-звіту, а також налаштовано автоматичний запуск тестів у GitHub Actions, який коректно показує як успішні, так і помилкові результати.
