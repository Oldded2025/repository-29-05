# 📝 Django Notes — простое приложение для заметок

Пошаговый гайд по созданию приложения для заметок на Django с нуля.

**Статус проекта:** репозиторий создан, виртуальное окружение активировано, Django установлено, `requirements.txt` и `.gitignore` на месте. Теперь пишем сам проект.

---

## 📋 Содержание

1. [Шаг 1 — Создание Django-проекта](#шаг-1--создание-django-проекта)
2. [Шаг 2 — Создание приложения notes](#шаг-2--создание-приложения-notes)
3. [Шаг 3 — Регистрация приложения в настройках](#шаг-3--регистрация-приложения-в-настройках)
4. [Шаг 4 — Настройка языка и часового пояса](#шаг-4--настройка-языка-и-часового-пояса)
5. [Шаг 5 — Создание модели Note](#шаг-5--создание-модели-note)
6. [Шаг 6 — Миграции](#шаг-6--миграции)
7. [Шаг 7 — Регистрация модели в админ-панели](#шаг-7--регистрация-модели-в-админ-панели)
8. [Шаг 8 — Создание суперпользователя](#шаг-8--создание-суперпользователя)
9. [Шаг 9 — Создание представления (view)](#шаг-9--создание-представления-view)
10. [Шаг 10 — Настройка URL-маршрутов](#шаг-10--настройка-url-маршрутов)
11. [Шаг 11 — Создание HTML-шаблона](#шаг-11--создание-html-шаблона)
12. [Шаг 12 — Запуск и проверка](#шаг-12--запуск-и-проверка)
13. [Шаг 13 — Сохранение зависимостей и коммит](#шаг-13--сохранение-зависимостей-и-коммит)
14. [Структура проекта](#структура-проекта)
15. [FAQ — решение частых проблем](#faq--решение-частых-проблем)

---

## Шаг 1 — Создание Django-проекта

Мы находимся в корне репозитория, виртуальное окружение уже активировано.

Команда `startproject` создаёт скелет Django-проекта — файлы настроек, точку входа и т.д. Точка в конце команды означает «создать проект в текущей директории» (без создания дополнительной вложенной папки).

```bash
django-admin startproject notes_prj .
```

После выполнения появится структура:

```
notes_prj/          ← директория с настройками проекта
├── __init__.py
├── settings.py     ← главный файл настроек
├── urls.py         ← главные URL-маршруты
├── wsgi.py
└── asgi.py
manage.py           ← скрипт для управления проектом
```

> **Что такое `manage.py`?** Это ваш главный инструмент разработчика. Через него запускается сервер, создаются миграции, управляется база данных и не только.

---

## Шаг 2 — Создание приложения notes

В Django проект состоит из **приложений** (apps). Проект — это контейнер, а приложение — конкретная функциональность. У нас одна функциональность — заметки, значит одно приложение `notes`.

```bash
python manage.py startapp notes
```

Появится директория:

```
notes/                  ← наше приложение
├── __init__.py
├── admin.py            ← настройки админ-панели для моделей этого приложения
├── apps.py             ← конфигурация приложения
├── models.py           ← описание моделей (таблиц базы данных)
├── views.py            ← логика обработки запросов
├── tests.py            ← тесты
└── migrations/         ← файлы миграций базы данных
    └── __init__.py
```

---

## Шаг 3 — Регистрация приложения в настройках

Django не «видит» приложения автоматически — их нужно явно зарегистрировать.

Открываем файл `notes_prj/settings.py`, находим список `INSTALLED_APPS` и добавляем `'notes'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes',  # ← добавляем наше приложение
]
```

> **Зачем это нужно?** Без этого Django не будет знать о существовании наших моделей, шаблонов и миграций из приложения `notes`.

---

## Шаг 4 — Настройка языка и часового пояса

В том же файле `notes_prj/settings.py` находим и меняем:

```python
LANGUAGE_CODE = 'ru-ru'          # было 'en-us'
TIME_ZONE = 'Europe/Moscow'      # было 'UTC'
```

Теперь админ-панель и все системные сообщения будут на русском языке, а даты — в московском часовом поясе.

---

## Шаг 5 — Создание модели Note

**Модель** — это Python-класс, который описывает таблицу в базе данных. Каждое поле класса становится столбцом таблицы.

Открываем `notes/models.py` и заменяем всё содержимое:

```python
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

**Что здесь происходит:**

| Элемент | Описание |
|---------|----------|
| `title` | Строковое поле максимум 200 символов — заголовок заметки |
| `body` | Текстовое поле без ограничения длины — тело заметки |
| `created_at` | Дата и время создания. `auto_now_add=True` — заполняется автоматически при создании |
| `updated_at` | Дата и время последнего изменения. `auto_now=True` — обновляется автоматически при каждом сохранении |
| `class Meta` | Настройки модели: как она называется в админке и в каком порядке сортируются записи |
| `__str__` | Определяет, как объект будет отображаться в текстовом виде (в админке, в консоли) |

---

## Шаг 6 — Миграции

Миграции — это механизм Django для синхронизации моделей (код Python) и базы данных (таблицы SQL). Нужно сделать два шага:

**6.1 — Создать файл миграции** (Django проанализирует модели и сгенерирует инструкции):

```bash
python manage.py makemigrations notes
```

Результат:
```
Migrations for 'notes':
  notes/migrations/0001_initial.py
    + Create model Note
```

**6.2 — Применить миграцию** (выполнить SQL-инструкции, создать таблицу в базе):

```bash
python manage.py migrate
```

Результат — список применённых миграций, каждая со статусом `OK`:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, notes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
  Applying notes.0001_initial... OK
  ...
```

> **Когда запускать миграции?**
> - При первом запуске проекта
> - После каждого изменения моделей (добавление/изменение/удаление полей)
> - После `git pull`, если кто-то из команды изменил модели

---

## Шаг 7 — Регистрация модели в админ-панели

Django поставляется с мощной админ-панелью из коробки. Но модели нужно регистрировать явно.

Открываем `notes/admin.py` и заменяем содержимое:

```python
from django.contrib import admin
from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
```

**Что здесь:**

| Параметр | Описание |
|----------|----------|
| `list_display` | Какие столбцы отображаются в списке заметок |
| `search_fields` | По каким полям работает поиск в админке |

Теперь в админ-панели можно будет видеть список заметок с заголовком и датами, а также искать заметки по заголовку и тексту.

---

## Шаг 8 — Создание суперпользователя

Суперпользователь — это учётная запись администратора с полным доступом к админ-панели.

```bash
python manage.py createsuperuser
```

Вводим данные (при вводе пароля символы **не отображаются** — это нормально, просто набираем вслепую):

```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

> ⚠️ Запомните логин и пароль! Они понадобятся для входа в админ-панель.

---

## Шаг 9 — Создание представления (view)

**Представление (view)** — это функция, которая принимает HTTP-запрос и возвращает ответ (обычно HTML-страницу).

Открываем `notes/views.py` и заменяем содержимое:

```python
from django.shortcuts import render
from notes.models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})
```

**Что здесь происходит:**

1. `Note.objects.all()` — получаем все заметки из базы данных
2. `render(...)` — рендерим HTML-шаблон `notes/note_list.html`, передавая в него переменную `notes`

---

## Шаг 10 — Настройка URL-маршрутов

URL-маршруты определяют, какая функция (view) будет обрабатывать запрос на определённый адрес.

**10.1 — Создаём `notes/urls.py`** (файл маршрутов приложения):

```python
from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
]
```

Здесь корневой адрес `''` (то есть `/`) обрабатывается функцией `note_list`.

**10.2 — Подключаем маршруты приложения в главном файле `notes_prj/urls.py`:**

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),  # ← подключаем URL-ы приложения notes
]
```

Функция `include()` позволяет «вложить» маршруты одного приложения в общий список маршрутов проекта.

---

## Шаг 11 — Создание HTML-шаблона

Шаблоны Django хранятся в папках `templates/` внутри приложений. Django ищет шаблоны автоматически, если соблюдена структура папок.

**11.1 — Создаём директорию для шаблонов:**

```bash
mkdir notes\templates\notes
```

> Вложенная папка `notes` внутри `templates` — это лучшая практика. Она предотвращает конфликты имён, если два разных приложения имеют шаблон с одинаковым именем.

**11.2 — Создаём файл `notes/templates/notes/note_list.html`:**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мои заметки</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }
        .note { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .note h2 { margin-top: 0; color: #333; }
        .note p { color: #666; }
        .note .date { font-size: 0.8em; color: #999; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .admin-link { text-decoration: none; color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Список заметок</h1>
        <a href="{% url 'admin:index' %}" class="admin-link">Управление заметками</a>
    </div>

    {% if notes %}
        {% for note in notes %}
            <div class="note">
                <h2>{{ note.title }}</h2>
                <p>{{ note.body }}</p>
                <div class="date">Создано: {{ note.created_at|date:"d.m.Y H:i" }}</div>
            </div>
        {% endfor %}
    {% else %}
        <p>Пока нет ни одной заметки.</p>
    {% endif %}
</body>
</html>
```

**Основы шаблонизатора Django:**

| Конструкция | Значение |
|-------------|----------|
| `{{ переменная }}` | Вывод значения переменной |
| `{% for note in notes %}` | Цикл по списку |
| `{% if notes %}` | Условие |
| `{% url 'admin:index' %}` | Генерация URL по имени маршрута |
| `{{ date\|date:"d.m.Y H:i" }}` | Фильтр форматирования даты |

---

## Шаг 12 — Запуск и проверка

**12.1 — Запускаем сервер:**

```bash
python manage.py runserver
```

При успешном запуске:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues.
Django version 6.0.5, using settings 'notes_prj.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**12.2 — Открываем в браузере:**

| Страница | URL | Что должно быть |
|----------|-----|-----------------|
| Главная (список заметок) | http://127.0.0.1:8000/ | «Пока нет ни одной заметки.» |
| Админ-панель | http://127.0.0.1:8000/admin/ | Форма входа |

**12.3 — Добавляем первую заметку:**

1. Заходим в админ-панель (`/admin/`) под логином и паролем суперпользователя
2. На главной странице админки видим раздел **«Заметки»**
3. Нажимаем **«+ Добавить»** рядом с «Заметки»
4. Заполняем «Заголовок» и «Текст заметки»
5. Нажимаем **«Сохранить»**

**12.4 — Проверяем:**

Обновляем главную страницу (`/`) — теперь там должна отображаться созданная заметка с заголовком, текстом и датой создания.

🎉 **Приложение работает!**

---

## Шаг 13 — Сохранение зависимостей и коммит

**13.1 — Сохраняем список зависимостей в `requirements.txt`:**

```bash
pip freeze > requirements.txt
```

Эта команда записывает все установленные пакеты с точными версиями. Теперь любой разработчик (или вы сами на другом компьютере) сможет восстановить окружение командой:

```bash
pip install -r requirements.txt
```

**13.2 — Коммитим изменения:**

```bash
git add .
git commit -m "feat: базовое приложение для заметок

- Создан проект notes_prj и приложение notes
- Модель Note с полями title, body, created_at, updated_at
- Представление для списка заметок
- HTML-шаблон с базовой стилизацией
- Русский язык и московское время в настройках
- Модель зарегистрирована в админ-панели
- Зависимости сохранены в requirements.txt"
```

---

## 📁 Структура проекта

Итоговая структура после всех шагов:

```
django_simple_project/
├── .venv/                     # Виртуальное окружение (в .gitignore!)
├── .git/                      # Данные Git
├── .gitignore                 # Игнорируемые файлы
├── manage.py                  # Скрипт управления проектом
├── README.md                  # Этот файл
├── requirements.txt           # Зависимости Python
│
├── notes_prj/                 # Настройки проекта
│   ├── __init__.py
│   ├── settings.py            # Настройки: INSTALLED_APPS, БД, язык, время
│   ├── urls.py                # Главные URL-маршруты (admin + notes)
│   ├── wsgi.py                # Точка входа для production-сервера
│   └── asgi.py                # Точка входа для async-сервера
│
├── notes/                     # Приложение «Заметки»
│   ├── __init__.py
│   ├── admin.py               # Регистрация Note в админ-панели
│   ├── apps.py                # Конфигурация приложения
│   ├── models.py              # Модель Note
│   ├── views.py               # Функция note_list
│   ├── urls.py                # URL-маршруты приложения
│   ├── tests.py               # Тесты (пусто)
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py    # Миграция — создание таблицы Note
│
├── notes/templates/           # HTML-шаблоны
│   └── notes/
│       └── note_list.html     # Шаблон списка заметок
│
└── db.sqlite3                 # База данных SQLite (создаётся при migrate)
```

---

## ❓ FAQ — решение частых проблем

### `'python' is not recognized as an internal or external command`
Python не добавлен в PATH. На Windows попробуйте `py` вместо `python`.

### `No module named 'django'`
Забыли активировать виртуальное окружение или установить Django:
```bash
.venv\Scripts\activate
pip install django
```

### `You have unapplied migrations`
Забыли применить миграции:
```bash
python manage.py migrate
```

### `Error: That port is already in use`
Порт 8000 занят. Запустите на другом:
```bash
python manage.py runserver 9000
```

### Страница открывается, но выглядит «голой» (без стилей)
Убедитесь, что шаблон лежит именно здесь: `notes/templates/notes/note_list.html`.

### `DisallowedHost` при запуске с другого устройства
Добавьте ваш IP в `ALLOWED_HOSTS` в `notes_prj/settings.py`:
```python
ALLOWED_HOSTS = ['192.168.1.100']
```

### Ничего не работает — что делать?
Выполните всё по порядку с нуля:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Если проблема сохраняется — скопируйте **полный текст ошибки из терминала** и обратитесь к преподавателю.

---

## 📚 Полезные ссылки

- [Документация Django (EN)](https://docs.djangoproject.com/)
- [Документация Django (RU)](https://djangoproject.com.ru/) — неполная, но полезная
- [Документация Python](https://docs.python.org/3/)
- [SQLite Browser](https://sqlitebrowser.org/) — программа для просмотра `.db` файлов

---

*Проект создан в учебных целях. Приятного изучения Django! 🎓*
