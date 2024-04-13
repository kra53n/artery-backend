# ***`artery-backend`***

***`artery-backend`*** is a part of the `Artery` application together
with [***`artery-frontend`***](https://github.com/fekoneko/artery-frontend/).

## Usage

> [!NOTE]
> Available api adresses located in the `artery/api/views.py` file.

### Install Python packages

```
pip install -q requirements.txt
```

### Set database

1. Install MySql database
2. Run MySql
3. Create database with `artery` name
4. Fill `artery/config/mysql.cnf` file

### Run server

Go to the `artery` directory and run follow commands:

```
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver
```

## Authors

### Backend

- [kra53n](https://github.com/kra53n/)
- [C0ldSt33l](https://github.com/c0ldst33l/)

### Frontend

- [fekoneko](https://github.com/fekoneko/)
- [MattKenyei](https://github.com/MattKenyei)
