# Yatube
## Проект социальной сети

### Описание:
Проект Yatube представляет собой полноценную площадку для публикации постов и ведения блогов — с авторизацией, персональными лентами, с комментариями и подпиской на авторов.

### Технологический стэк:
Python 3.8.8
Django
HTML

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone ...
cd api_final_yatube
```
## Cоздать и активировать виртуальное окружение:
```bash
python -m venv env
source venv/Scripts/activate
```
## Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Выполнить миграции:
```bash
python manage.py migrate
```
## Запустить проект:
```bash
python manage.py runserver  
```
