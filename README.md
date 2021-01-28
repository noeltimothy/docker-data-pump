# Docker Data Pump Service
## Oerview

This service performs a Dynamo DB Query and posts the results of the query to a POST URL that is provided by the user. 
This is implemented within a docker container and all input is passed using environment variable passed to the Docker container.

## How to build?

- As a pre-requisite you will need to have Docker installed on your Linux system.
- Next, pull this repo and build a docker image

```
# sudo apt install -y docker.io
# git clone https://github.com/noeltimothy/docker-data-pump
# cd docker-data-pump
# sudo docker build -t docker_pump .
```

## How to configure?

This docker container requires the following inputs in the provided env file to run successfuly.
An example env file is already present in this repo

- AWS_KEY : This is the AWS key to your account
- AWS_SECRET: This is the AWS secret to your account
- AWS_REGION: You can specify the AWS region such as 'us-east-2'
- DYNAMO_TABLE: This is the name of an existing Dynamo DB on your AWS account within the region you provided
- DYNAMO_QUERY_KEY: The Dynamo query searches the above table using this key
- DYNAMO_QUERY_VALUE: The Dynamo query searches the above table to match this value
- POST_URL: This is the URL where the results will be posted
- SLEEP_TIME: This is the time in minutes between executions of this service


## How to run?

``
sudo docker run --env-file=env -d --name docker_pump docker_pump:latest
```

## Troubleshooting

You can use docker logs to see log messages

```
sudo docker logs docker_pump
```

