# Continuous Integration with Jenkins Pipelines
# Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Repository structure](#repository-structure)
4. [Jenkins usage and configuration](#jenkins-usage-and-configuration)
5. [Pipelines tl;dr](#pipelines-tldr)
6. [Add vim-instance](#add-vim-instance)
7. [Add integration-test](#add-integration-test)
8. [TODO](#todo)

## Introduction
With multiple possible deployment configurations and multiple test suits to cover most use cases, testing gets overwhelmingly complex.

To achieve continuous integration and delivery the used automation technique should be flexible and extend able. We will be using Jenkins new [Declarative Pipelines](https://jenkins.io/doc/book/pipeline/) and [Docker Compose](https://docs.docker.com/compose/) to provide the possibility of automatic package buildlng, build checking and testing of different system under test against the already existing [integration-tests](https://github.com/openbaton/integration-tests)
## Setup
This has been tested on the following deployment
- `Ubuntu 16.04`
- `Jenkins 2.60.2`
- `Docker 17.06.0-ce`
- `Docker Compose 1.14.0`
- `OpenStackClient 3.12`
- `OSPurge 2.0`

### Docker and Docker-Compose
Install Docker-CE
```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
```
And Docker-compose
```bash
sudo apt-get install python3-pip
sudo pip3 install docker-compose
```
Also add your user to the docker group
```bash
sudo usermod -aG docker $USER
```
### Jenkins
Install Jenkins via the official package repositories
```bash
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
```
Do the initial configure steps, go to `http://IP_OF_JENKINS:8080`, get the needed key from `/var/log/jenkins/jenkins.log`, choose a username and password for the admin user and skip through the default configuration.

## Repository structure
- `master`: contains this README
- `build-docker`: builds docker container for all java components, branch to be build selectable
- `run-every_night`: runs test-main every night with predefined parameters
- `test-main`: entry point pipeline to run integration tests
- `test-dummy`: sub job to run the relevant tests for amqp/rest vnfm
- `test-generic`: sub job to run the relevant tests for generic
- `test-arbitrary-branches`: entry point pipeline to run tests against self defined branch compositions
- `test-bootstrap-config`: entry point pipeline to run the bootstrap install script against multiple configurations and distributions
- `test-db_upgrade`: entry point pipeline to check if the database migration between two tags or branches works correctly

This repository is added as a [Multibranch Pipeline](https://jenkins.io/doc/book/pipeline/multibranch/). All repositories including a pipeline must include a single `Jenkinsfile`. Jenkins automatically pulls the branch on run and then executes the found `Jenkinsfile`. New branches will be found as well.

## Jenkins usage and configuration
### Integration tests
To run the integration test suite manually against a docker-compose system under test, start the `test-main` pipeline with parameters (drop down point+click).

### Environment variables
Because the integration tests need some "node specific" configuration (i.e. real-vim file, configuration file, ssh-key), paths to the files in `misc` branch are setup as environmental variables in the jenkins master node. This way, they are easily accessible in the pipeline steps, for example regarding the actual host ip or path to the private key. Those can be set up through `Manage Jenkins -> Manage Nodes -> Settings wheel -> Node properties`, in our case the master node.

#### Used environment variables
- `HOST_IP`: IP of the node (needed for ems and docker-compose)
- `INTEGRATION_TESTS_CONFIG`: Path to integration-tests configuration
- `PEM_FILE`: Path to ssh private key
- `VIM_FILES`: Path to vim files

## Pipelines tldr
### Docker compose files
- `min-compose`: nfvo, generic/dummy-rest/dummy-amqp vnfms, rabbitmq, mysql
- `min_nomysql-compose`: as above, but with in memory db (fastest deploy)
- `full-compose`: Full deployment with all external components. No sense in using yet as there are no tests for the components

### Periodic or hooked builds
To set a pipeline to automatically build based on cron-style times, see the example pipeline for [every night](https://github.com/openbaton/openbaton-ci/blob/dd58f3f88719edee5b453fd2aac34bad95da7c0a/Jenkinsfile#L8). The syntax is described [here](https://jenkins.io/doc/book/pipeline/syntax/#triggers). If unfamiliar with cron-style strings, check [here](https://crontab-generator.org/).

Relevant links for webhook based integrations:
- https://thepracticalsysadmin.com/setting-up-a-github-webhook-in-jenkins/
- https://gist.github.com/misterbrownlee/3708738

The current implementation of the `after commit` trigger is polling the relevant repositories every 5 minutes and only starts a test-run if changes are detected.

## Add vim-instance
Add the JSON file to the correct folder on your deployment, as configured in the environment variables. As naming convetion, use the IP of the used testbed. Add the name (without .json suffix) to the choice parameter in [test-main](https://gitlab.fokus.fraunhofer.de/openbaton/openbaton-ci/blob/525079b7808ff73ef4c9ec2f4d397930575dda43/Jenkinsfile#L31). It will be available after the next scm checkout of this branch.

## Add integration-test
After adding the test to the integration-tests, add a new stage corresponding to the new scenario to either the [vnfm-dummy](https://gitlab.fokus.fraunhofer.de/openbaton/openbaton-ci/tree/test-dummy) or [vnfm-generic](https://gitlab.fokus.fraunhofer.de/openbaton/openbaton-ci/tree/test-generic) Pipeline.

When running e.g. `test-main` be sure to include `trigger build` as seen in this image. This is needed because the integration-test container has to be rebuild to include any changes.
![](./img/trigger-build.png)

### Add it to the parameters
Include it in the possible `TEST_SET` [choices](https://gitlab.fokus.fraunhofer.de/openbaton/openbaton-ci/blob/26c2cc845dca79cb5930638a94de17ef0a27a924/Jenkinsfile#L6)
### Add a new stage
Include a new stage, similar to the already [existing](https://gitlab.fokus.fraunhofer.de/openbaton/openbaton-ci/blob/26c2cc845dca79cb5930638a94de17ef0a27a924/Jenkinsfile#L83).

If the test should be included when run with `TEST_SET=all`, set the `when` expression accordingly. E.g

```groovy
when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'new-test'} }
```
