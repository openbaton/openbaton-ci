FROM openjdk:8-jdk
COPY . /libs
WORKDIR /libs/nfvo
RUN ./gradlew :common:install
RUN ./gradlew :catalogue:install
WORKDIR /libs/client
RUN ./gradlew :sdk:install
WORKDIR /libs/plugin
RUN ./gradlew install
WORKDIR /libs
RUN ./gradlew install
