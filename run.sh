sudo docker stop test
sudo docker rm test
sudo docker build -t test .
sudo docker run --env-file=env -d --name test test:latest
