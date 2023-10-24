# Приложение для Благотворительного фонда поддержки котиков QRKot

## Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Доступно формирование отчета о закрытых проектах в Google Sheets

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AlexBatanov/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Создать и заполнить .env

```
APP_TITLE=QRKot
DESCRIPTION=Описание проекта
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
# для google api
TYPE=service_account
PROJECT_ID=project_id
PRIVATE_KEY_ID=private_ky_id
PRIVATE_KEY=private_key
CLIENT_EMAIL=youremail@rapid-rite.iam.gserviceaccount.com
CLIENT_ID=client_id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your_service_name>
EMAIL=youremail@gmail.com

```

Запуск проекта
```
uvicorn app.main:app --reload
```

Подробная документация
```
http://localhost:8000/docs
```

### Автор
[Batanov Alexandr](https://github.com/AlexBatanov)