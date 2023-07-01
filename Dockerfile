FROM python:3

COPY . /home/karim_123/app

WORKDIR /home/karim_123/app

RUN pip install django

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
