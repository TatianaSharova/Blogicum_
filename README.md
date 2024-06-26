# Blogicum  
Blogicum - это социальная сеть для публикации личных дневников.

Функционал проекта:  
На сайте блогикума пользователь может создать свою страницу и публиковать на ней посты.   
Для каждого поста нужно указать категорию — например «путешествия», «кулинария» или «python-разработка», а также опционально локацию, с которой связан пост, например «Остров отчаянья» или «Караганда».   
Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся.  
Пользователи смогут заходить на чужие страницы, читать и комментировать чужие посты.
Для своей страницы автор может задать имя и уникальный адрес.  
Для проекта настроена админ-зона.  

Для проекта был написан фронт на HTML.

### **Используемые технологии**

![HTML5](https://a11ybadges.com/badge?logo=html5)
![Django](https://a11ybadges.com/badge?logo=django)
![Python](https://a11ybadges.com/badge?logo=python)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Локальный запуск проекта:

**_Склонировать репозиторий к себе_**
```
git@github.com:TatianaSharova/blogicum_.git
```
**_Создать в корне проекта файл .env и поместить туда SECRET_KEY:_**
```
SECRET_KEY = 'ваш secret key'
```

**_Создать и активировать виртуальное окружение:_**

Для Linux/macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Для Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
**_Установить зависимости из файла requirements.txt:_**
```
pip install -r requirements.txt
```
**_Выполнить миграции:_**
```
python manage.py migrate
```
**_Создать суперюзера:_**
```
python manage.py createsuperuser
```
**_Запустить проект:_**
```
python manage.py runserver
```

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)