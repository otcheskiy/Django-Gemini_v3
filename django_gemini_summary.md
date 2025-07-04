
# Django-Gemini: Хронология и структура проекта

## 📌 Цели проекта
- Создание Django-приложения с каталогом товаров и изображениями.
- Реализация REST API для взаимодействия с 1С.
- Подключение Bootstrap и семантической HTML-вёрстки.
- Настройка повторно используемых шаблонов (base.html, navbar.html).
- Развёртывание проекта на хостинге.
- Настройка Git и GitHub.
- Подключение авторизации по токену и тестовая интеграция с 1С.

---

## ✅ 1. Старт проекта
- Создан Django-проект `Django-Gemini_v2` с приложениями `catalog` и `myshop`.
- Настроено виртуальное окружение `venv`.
- Установлены зависимости: `Django`, `djangorestframework`, `Pillow` и др.

---

## ✅ 2. Модели и API
- Модель `Product` с полями: `name`, `price`, `stock`, `image`, `code_1c`, `categories`, `slug`.
- Модель `Category`.
- API с использованием `ModelViewSet` и `DefaultRouter`.
- Пути API:
  - `/api/v1/products/`
  - `/api/v1/categories/`
- Сериализаторы: `ProductSerializer`, `CategorySerializer`.

---

## ✅ 3. HTML-интерфейс
- Шаблон `product_list.html` с Bootstrap 5.
- Использована семантическая вёрстка (`<main>`, `<section>`, `<article>`).
- Карточки товаров с Bootstrap (`.card`).
- Добавлена пагинация.

---

## ✅ 4. Шаблоны
- `base.html`: основной макет с Bootstrap и блоками `{% block title %}`, `{% block content %}`.
- `navbar.html`: навигационное меню, подключается через `{% include 'navbar.html' %}`.
- Использовано `{% extends 'base.html' %}` во всех шаблонах.

---

## ✅ 5. Медиа и статика
- Настроены `MEDIA_URL` и `MEDIA_ROOT`.
- Добавлено отображение изображений в шаблонах.
- Настроен `STATIC_ROOT`, выполнена команда `collectstatic`.

---

## ✅ 6. Развёртывание на хостинге (Beget)
- Указан `ALLOWED_HOSTS` в `settings.py`.
- Подключена база данных MySQL (Beget) вместо SQLite.
- Прописаны корректные пути к `STATIC_ROOT`, `MEDIA_ROOT`.
- Настроен `wsgi.py`, окружение и домен.

---

## ✅ 7. Работа с Git и GitHub
- Создан репозиторий [Django-Gemini_v2](https://github.com/otcheskiy/Django-Gemini_v2).
- Привязан новый `origin`, сделан `push`:
  ```bash
  git remote set-url origin https://github.com/otcheskiy/Django-Gemini_v2.git
  git push -u origin main
  ```

---

## ✅ 8. Интеграция с 1С и архитектура
### Вариант 1 (используется):
- 1С → Django: выгрузка данных в JSON через HTTP-запрос.
- Django принимает и обрабатывает данные через API.

### Вариант 2 (не выбран):
- Django → 1С: обращение к веб-сервису 1С.
- Более сложно в инфраструктуре и безопасности.

---

## ✅ 9. Авторизация и синхронизация
- Подключена авторизация API по токену (`rest_framework.authtoken`).
- Реализована тестовая выгрузка данных из 1С на сайт через API.

---

## 📦 Пример `.gitignore`

```gitignore
venv/
__pycache__/
*.pyc
db.sqlite3
media/
static/
.idea/
```
