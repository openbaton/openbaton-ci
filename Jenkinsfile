#!/usr/bin/env groovy
pipeline {
    parameters {
        choice(
            name: 'TEST_SET',
            choices: 'all\nscenario-docker-deploy\nscenario-docker-iperf\nsimple',
            description: 'Integration tests to run'
        )
        string(
            name: 'BRANCH',
            defaultValue: 'latest',
            description: 'tag, e.g. latest, 4.0.0, 5.0, ...'
        )
    }

    agent any

    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
    }

    stages {
        stage('Run scenario-docker-deploy') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-docker-deploy' || params.TEST_SET == 'simple' } }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} scenario-docker-deploy.ini"
            }
        }
        stage('Run scenario-docker-iperf') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-docker-iperf' } }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} scenario-docker-iperf.ini"
            }
        }
    post {
        failure {
            /* TODO: save log files */
            archive '*.log'
        }
    }
}
