# Topcon Positioning Project

### Требования
1. Python 3.5
2. Django 2.1.5

### Запуск
При первом запуске или после обновления:
```bash
python src/dj_back/manage.py collectstatic
python src/dj_back/manage.py migrate
python src/dj_back/manage.py runserver
```
 
При обычном запуске:
```bash
python src/dj_back/manage.py runserver
```

После этого должен запуститься сервер по
адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

На данный момент запускалось только на линуксе.
