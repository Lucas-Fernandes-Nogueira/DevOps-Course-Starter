echo $DOCKER_PASSWORD | docker login -u $DOCKER_ID --password-stdin
docker build --target production --tag lucnog/todo-app:$TRAVIS_COMMIT .
docker push lucnog/todo-app:$TRAVIS_COMMIT
docker tag lucnog/todo-app:$TRAVIS_COMMIT lucnog/todo-app:latest
docker push lucnog/todo-app:latest
