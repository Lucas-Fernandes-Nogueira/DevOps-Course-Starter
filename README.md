# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
### Setup .env file
1. Make a copy of .env.template in the root folder and rename it to .env (this is a one-time operation on first setup).
    ```bash
    $ cp .env.template .env  # (first time only)
    ```
    The `.env` file is used by flask to set environment variables when running `flask run`. In the next step you'll set the required variables.

2. Fill in the API_KEY, TOKEN, and BOARD_ID with your Trello account credentials and Board id. (you can generate these credentials by going to https://trello.com/app-key)

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

## Running the App

Once all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Virtual Machine
If you have Vagrant installed in your machine, provision and run a virtual machine with the command:
```bash
$ vagrant up
```
This will automatically launch the app, which you can also view in your [`browser`](http://localhost:5000/).

## Running with Docker
### Dev
In developer mode, Flask tracks changes to the files in the codebase. You should see the changes after a simple tab refresh, without the need to rebuild the docker image.

To run in developer mode, first build the docker image with the following command from the project directory:
```bash
docker build --target development --tag todo-app:dev .
```
After you've built the image, run the website with the following command:
```bash
docker run -p 5000:5000 --env-file .env --mount type=bind,source="$(pwd)",destination=/todo-app todo-app:dev
```
Now visit http://localhost:5000/ in your web browser to view the app.
### Production
To run in production mode, first build the image with the following command:
```bash
docker build --target production --tag todo-app:prod .
```
Then run the website with the following:
```bash
docker run -p 5000:5000 --env-file .env todo-app:prod
```
Now visit http://localhost:5000/ in your web browser to view the app.
### Other Useful commands
Stop all running containers:
```bash
docker stop $(docker ps -a -q)
```






## Run the Tests
If you want to run all tests, use the following command:
```bash
$ pytest
```

If you want to run the test suits individually, you just need to run the appropriate command from the project root:

### Unit Tests
```bash
$ pytest test_indexViewModel.py
```
### Integration Tests
```bash
$ pytest test_app.py    
```
### End to End tests
Before you run the End to End tests you need to download the mozilla geckodriver executable ([`here`](https://github.com/mozilla/geckodriver/releases)) and add it to your path. (In my case, I downloaded "geckodriver-v0.28.0-win64.zip", extracted the executable to a new geckodriver folder, and added the directory to the path).

Then run the following command:
```bash
$ pytest test_e2e.py       
```

## Common issues and Gotchas
1. The Trello board should contain three lists with the following names:
    * To Do
    * Doing
    * Done

