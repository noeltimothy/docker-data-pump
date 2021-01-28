FROM ubuntu:18.04
RUN apt-get update && \
apt-get install -y python3-pip

RUN pip3 install requests boto3

WORKDIR base
COPY . ./
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
