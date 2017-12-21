#!/usr/bin/env groovy
pipeline {
    parameters {
        choice(
            name: 'TEST_SET',
            choices: 'all\nscenario-real-iperf\nscenario-complex-ncat\nscenario-scaling\nerror-in-configure\nerror-in-instantiate\nerror-in-start\nerror-in-terminate\nwrong-lifecycle-event\nscenario-real-sipp-fms-heal\nsimple',
            description: 'Integration tests to run'
        )
        string(
            name: 'VIM_LOCATION',
            defaultValue: 'pop',
            description: 'Which Openstack testbed to use'
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

        stage('Run scenario-real-iperf') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-real-iperf' || params.TEST_SET == 'simple'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} scenario-real-iperf.ini"
            }
        }
        stage('Run scenario-complex-ncat') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-complex-ncat'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} scenario-complex-ncat.ini"
            }
        }
        stage('Run scenario-scaling') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'scenario-scaling'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} scenario-scaling.ini"
            }
        }
        stage('Run error-in-configure') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'error-in-configure'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} error-in-configure.ini"
            }
        }
        stage('Run error-in-instantiate') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'error-in-instantiate'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} error-in-instantiate.ini"
            }
        }
        stage('Run error-in-start') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'error-in-start'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests  -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} error-in-start.ini"
            }
        }
        stage('Run error-in-terminate') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'error-in-terminate'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} error-in-terminate.ini"
            }
        }
        stage('Run wrong-lifecycle-event') {
            when { expression { params.TEST_SET == 'all' || params.TEST_SET == 'wrong-lifecycle-event'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} wrong-lifecycle-event.ini"
            }
        }
        stage('Run user-project-test') {
            when { expression { params.TEST_SET == 'user-project-test'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} user-project-test.ini"
            }
        }
        stage('Run stress-test') {
            when { expression { params.TEST_SET == 'stress-test'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} stress-test.ini"
            }
        }
        stage('Run fms-heal') {
            when { expression { params.TEST_SET == 'scenario-real-sipp-fms-heal'} }
            steps {
                sh "docker run -P --rm --name integration-tests -p 8181:8181 -v $CONFIG:/etc/openbaton/integration-tests -v $VIM_FILES/${params.VIM_LOCATION}.json:/etc/openbaton/integration-tests/vim-instances/real-vim.json openbaton/integration-tests:${params.BRANCH} scenario-real-sipp-fms-heal.ini"
            }
        }
    }

    post {
        failure {
            archive '*.log'
        }
    }
}
