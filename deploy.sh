echo $DOCKER_PASSWORD | docker login -u $DOCKER_ID --password-stdin
docker build --target production --tag lucnog/todo-app:$TRAVIS_COMMIT .
docker push lucnog/todo-app:$TRAVIS_COMMIT
docker tag lucnog/todo-app:$TRAVIS_COMMIT lucnog/todo-app:latest
docker push lucnog/todo-app:latest
docker tag lucnog/todo-app:latest registry.heroku.com/devops-todo-app/web
heroku container:login
docker push registry.heroku.com/devops-todo-app/web
heroku container:release web --app devops-todo-app