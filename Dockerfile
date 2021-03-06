FROM python:3.8.6-buster as base
RUN pip install "poetry==1.1.4"
WORKDIR /todo-app
EXPOSE 5000
COPY poetry.toml /todo-app
COPY poetry.lock /todo-app
COPY pyproject.toml /todo-app

FROM base as production
RUN poetry config virtualenvs.create false --local && poetry install --no-dev
COPY . /todo-app
CMD poetry run gunicorn --bind=0.0.0.0:$PORT "app:create_app()"

FROM base as development
RUN poetry config virtualenvs.create false && poetry install
CMD poetry run flask run --host=0.0.0.0 --port=5000

FROM base as test
# Install Chrome
RUN apt-get update
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
    apt-get install ./chrome.deb -y &&\
    rm ./chrome.deb
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
    echo "Installing chromium webdriver version ${LATEST}" &&\
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
    unzip ./chromedriver_linux64.zip
RUN poetry config virtualenvs.create false && poetry install
COPY . /todo-app
ENTRYPOINT ["poetry", "run", "pytest"]