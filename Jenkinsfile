#!/usr/bin/env groovy
pipeline {
    parameters {
        choice(
            name: 'TEST_SET',
            choices: 'all\nscenario-dummy-iperf\nscenario-many-dependencies\nuser-project-test\nstress-test\nsimple',
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
        stage('Run scenario-dummy-iperf') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-dummy-iperf' || params.TEST_SET == 'simple' } }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} scenario-dummy-iperf.ini"
            }
        }
        stage('Run scenario-many-dependencies') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-many-dependencies'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} scenario-many-dependencies.ini"
            }
        }
        stage('Run user-project-test') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'user-project-test'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} user-project-test.ini"
            }
        }
        stage('Run stress-test') {
            when { expression { params.TEST_SET == 'stress-test'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key openbaton/integration-tests:${params.BRANCH} stress-test.ini"
            }
        }
    }
    post {
        failure {
            /* TODO: save log files */
            archive '*.log'
        }
    }
}
