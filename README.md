# Useful commands

## Initialize

- **Command Prompt or PowerShell**:`.\initialize.bat`
- **macOS or Linux Terminal**: `source initialize.sh`

## Venv

- `python -m venv venv`
- **Command Prompt**: `.\venv\Scripts\activate`
- **PowerShell**: `.\venv\Scripts\Activate.ps1`
- **macOS or Linux Terminal**: `source venv/bin/activate`
- `deactivate`

## Pip

- `pip list`
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `pip uninstall -r requirements.txt -y`

## Django

- `python populate.py`
- `python manage.py test apps`
- `python manage.py test apps core`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py collectstatic`
- `python manage.py createsuperuser`
- `python manage.py runserver`


# Docker

- `docker ps -a`
- `docker system prune -a`

## Docker-compose

- `docker-compose up -d --build`
- `docker-compose ps -a`
- `docker-compose logs`
- `docker-compose down -v`

## Terraform

- `.\terraform init`
- `.\terraform fmt`
- `.\terraform validate`
- `.\terraform plan -var-file=terraform.tfvars`
- `.\terraform apply -var-file=terraform.tfvars`
