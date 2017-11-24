#!/usr/bin/env groovy
pipeline {
    parameters {
        string(
            name: 'FROM',
            defaultValue: 'refs/tags/4.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>, leave empty to use last build'
        )
        string(
            name: 'TO',
            defaultValue: 'refs/heads/develop',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>, leave empty to use last build'
        )
    }

    agent any
    options {
        timeout(
            time: 20,
            unit: 'MINUTES'
        )
        disableConcurrentBuilds()
    }

    stages {
        stage('Clean workspace') {
            steps {
                sh 'rm -rf */ || true'
                sh 'rm -rf *.log || true'
            }
        }
        stage('Build images') {
            parallel {
                stage('Build "from" image') {
                    when { expression { params.FROM != '' } }
                    steps {
                        dir('from') {
                            checkout([$class: 'GitSCM', branches: [[name: params.FROM]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/NFVO.git']]])
                            sh 'if [ ! -f ./Dockerfile ];then cp ../Dockerfile ./;fi'
                            sh 'docker build . -t nfvo-from:local'
                        }
                    }
                }
                stage('Build "to" image') {
                    when { expression { params.TO != '' } }
                    steps {
                        dir('to') {
                            checkout([$class: 'GitSCM', branches: [[name: params.TO]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/NFVO.git']]])
                            sh 'if [ ! -f ./Dockerfile ];then cp ../Dockerfile ./;fi'
                            sh 'docker build . -t nfvo-to:local'
                        }
                    }
                }
            }
        }
        stage('Deploy "from" scenario') {
            steps {
                sh "sed -i 's#openbaton/nfvo:latest#nfvo-from:local#g' min-compose.yml"
                sh "docker-compose -p dbtest -f min-compose.yml up -d"
                sh "timeout 600 bash -c 'until curl -sSf http://localhost:8088; do sleep 10;done'"
                sh "for container in \$(docker-compose -p dbtest -f min-compose.yml ps|grep dbtest|grep nfvo_1|awk '{print \$1}');do docker logs \$container > from_\$container.log 2>&1;done"
            }
        }
        stage('Let "to" orchestrator migrate') {
            steps {
                sh "docker-compose -p dbtest -f min-compose.yml stop nfvo"
                sh "sed -i 's/nfvo-from:local/nfvo-to:local/g' min-compose.yml"
                sh "docker-compose -p dbtest -f min-compose.yml up -d --no-deps nfvo"
                sh "timeout 120 bash -c 'until curl -sSf http://localhost:8088; do sleep 10;done'"
                sh "for container in \$(docker-compose -p dbtest -f min-compose.yml ps|grep dbtest|grep nfvo_1|awk '{print \$1}');do docker logs \$container > inbetween_\$container.log 2>&1;done"
            }
        }
        stage('Let "to" orchestrator restart') {
            steps {
                sh "docker-compose -p dbtest -f min-compose.yml restart nfvo"
                sh "timeout 120 bash -c 'until curl -sSf http://localhost:8088; do sleep 10;done'"
            }
        }
    }
    post {
        always {
            script {
                sh "for container in \$(env COMPOSE_PROJECT_NAME=dbtest docker-compose -f min-compose.yml ps|grep dbtest|awk '{print \$1}');do docker logs \$container > to_\$container.log 2>&1;done"
                sh "env COMPOSE_PROJECT_NAME=dbtest docker-compose -f min-compose.yml down"
                archive '*.log'
            }
        }
    }
}
