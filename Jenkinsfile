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
        stage('Run scenarios') {
            steps {
                script {
                    if (params.TEST_SET == 'simple') {
                        test_set = 'scenario-dummy-iperf'
                    }
                    if (params.TEST_SET != 'all') {
                        test_set = test_set + '.ini'
                    } else {
                        test_set = ''
                    }
                    sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $PEM_FILE:/etc/openbaton/integration-test/integration-test.key -v $INTEGRATION_TESTS_CONFIG:/etc/openbaton/integration-tests/integration-tests.properties openbaton/integration-tests:${params.BRANCH} $test_set"
                }
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
