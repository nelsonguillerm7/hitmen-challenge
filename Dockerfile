FROM python:3.10

ENV APP_ROOT /app

COPY . ${APP_ROOT}/
WORKDIR ${APP_ROOT}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install & use pipenv
COPY Pipfile ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --skip-lock --system

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
