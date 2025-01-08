# Useful commands

## Virtual environment

- `python -m venv venv`
- **Windows**: `call venv/Scripts/activate`
- **Linux or Mac**: `source venv/bin/activate`
- `deactivate`

## Requirements

- `pip list`
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `pip uninstall -r requirements.txt -y`

## Django stuff

- `python populate.py`
- `python manage.py test apps`
- `python manage.py test apps core`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py collectstatic`
- `python manage.py createsuperuser`
- `python manage.py runserver`
