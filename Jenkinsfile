#!/usr/bin/env groovy
pipeline {
    options {
        disableConcurrentBuilds()
    }
    agent any
    triggers {
        cron('H 1 * * *')
    }
    stages {
        stage('Test min_nomysql scenario') {
            steps {
                build job: 'test-main', parameters: [string(name: 'SYSTEM_UNDER_TEST', value: 'dockervnfm-compose'), string(name: 'BRANCH', value: 'master'), booleanParam(name: 'TRIGGER_BUILD', value: true), string(name: 'TEST_SET', value: 'all'), string(name: 'VNFM_TO_TEST', value: 'generic'), string(name: 'VIM_LOCATION', value: 'pop')]
            }
        }
    }
    post {
        success {
            slackSend color: 'good', message: "RUN EVERY NIGHT - #$BUILD_NUMBER Pipeline success! (<$BUILD_URL|Open>)"
        }
        failure {
            slackSend color: 'danger', message: "RUN EVERY NIGHT - #$BUILD_NUMBER Pipeline failure! (<$BUILD_URL|Open>)"
        }
    }
}
