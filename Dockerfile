FROM jenkins/jenkins:lts
USER root
RUN curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.03.1-ce.tgz && tar --strip-components=1 -xvzf docker-17.03.1-ce.tgz -C /usr/local/bin
RUN apt update && apt install -y python3-pip && pip3 install docker-compose
ENV DOCKER_HOST=tcp://dockerhost:2376
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
USER jenkins
