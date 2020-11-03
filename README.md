# DevOps Apprenticeship: Project Exercise

## Getting started

### Setup .env file
1. Make a copy of .env.template in the root folder and rename it to .env
2. Fill in the API_KEY, TOKEN, and BOARD_ID with your Trello account credentials and Board id. (you can generate these credentials by going to https://trello.com/app-key)

Note: Your trello board should contain three lists with the names "To Do", "Doing" and "Done".

### Install dependencies
The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
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

## Run the Tests
You just need to run the appropriate command from the project root:
### Unit Tests
```bash
$ pytest test_indexViewModel.py
```
Integration Tests
```bash
$ pytest test_app.py    
```
End to End tests
```bash
$ pytest test_e2e.py       
```

## Common issues and Gotchas
1. The Trello board should contain three lists with the following names:
    * To Do
    * Doing
    * Done