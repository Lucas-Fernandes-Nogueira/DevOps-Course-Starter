FROM python:3.8.6-buster as base
RUN pip install "poetry==1.1.4"
WORKDIR /todo-app
EXPOSE 5000

FROM base as production
COPY poetry.toml /todo-app
COPY poetry.lock /todo-app
COPY pyproject.toml /todo-app
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY . /todo-app
CMD poetry run gunicorn --bind=0.0.0.0:5000 "app:create_app()"

FROM base as development
COPY poetry.lock /todo-app
COPY pyproject.toml /todo-app
RUN poetry config virtualenvs.create false && poetry install
CMD poetry run flask run --host=0.0.0.0 --port=5000