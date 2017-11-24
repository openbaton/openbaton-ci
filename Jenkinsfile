#!/usr/bin/env groovy
pipeline {
    agent any
    stages {
        stage('Generate configurations') {
            steps {
                sh 'curl http://get.openbaton.org/bootstrap > bootstrap.sh'
                dir('cfg') {
                    sh 'rm -f *'
                    sh '../config_fuzzer.py'
                }
            }
        }
        stage('Build base-images') {
            parallel {
                stage('Build xenial') {
                    steps {
                        dir('xenial') {
                            sh 'docker build -t test-base:xenial .'
                        }
                    }
                }
                stage('Build trusty') {
                    steps {
                        dir('trusty') {
                            sh 'docker build -t test-base:trusty .'
                        }
                    }
                }
            }
        }
        stage('Run tests') {
            parallel {
                stage('Test configurations xenial') {
                    steps {
                        sh "for f in cfg/cfg*;do docker run --rm -h openbaton -v \$(pwd)/\$f:/config -v \$(pwd)/bootstrap.sh:/bootstrap test-base:xenial bash -c 'service rabbitmq-server start;bash /bootstrap --config-file=/config'|| (echo Failed on \$(cat \$f) && exit 1); done"
                    }
                }
                stage('Test configurations trusty') {
                    steps {
                        sh "for f in cfg/cfg*;do docker run --rm -h openbaton -v \$(pwd)/\$f:/config -v \$(pwd)/bootstrap.sh:/bootstrap test-base:trusty bash -c 'service rabbitmq-server start;bash /bootstrap --config-file=/config'|| (echo Failed on \$(cat \$f) && exit 1); done"
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker rmi test-base:xenial test-base:trusty'
        }
    }
}
