#!/usr/bin/env groovy
pipeline {
    parameters {
        choice(
            name: 'SYSTEM_UNDER_TEST',
            choices: 'min_nomysql-compose\nmin-compose\nfull-compose\nstandalone',
            description: 'System under test to use'
        )
        choice(
            name: 'BRANCH',
            choices: 'master\n5.0\nlocal',
            description: 'Which version to use'
        )
        booleanParam(
            name: 'TRIGGER_BUILD',
            defaultValue: false,
            description: 'Build new images before running tests'
        )
        string(
            name: 'TEST_SET',
            defaultValue: 'complex',
            description: 'Run only the most "simple", the most "complex" tests, "all" or "scenario-name"'
        )
        choice(
            name: 'VNFM_TO_TEST',
            choices: 'all\ngeneric\ndummy-amqp',
            description: 'Which vnfms to test against'
        )
        string(
            name: 'VIM_LOCATION',
            defaultValue: 'pop',
            description: 'Which openstack testbed to use'
        )
    }

    agent any

    options {
        timeout(
            time: 1,
            unit: 'HOURS'
        )
        disableConcurrentBuilds()
    }

    stages {
        stage('Build images') {
            when { expression { params.TRIGGER_BUILD && params.BRANCH != 'local' } }
            steps {
                script {
                    if (params.SYSTEM_UNDER_TEST == 'standalone') {
                        build job: 'build-docker', parameters: [string(name: 'STANDALONE', value: 'refs/heads/' + params.BRANCH), string(name: 'NFVO', value: ''), string(name: 'VNFM_GENERIC', value: ''), string(name: 'VNFM_DUMMY_AMQP', value: ''), string(name: 'PLUGIN_VIMDRIVER_TEST', value: ''), string(name: 'PLUGIN_VIMDRIVER_OPENSTACK', value: ''), string(name: 'INTEGRATION_TESTS', value: '')]
                    } else {
                        build job: 'build-docker', parameters: [string(name: 'STANDALONE', value: ''), string(name: 'NFVO', value: 'refs/heads/' + params.BRANCH), string(name: 'VNFM_GENERIC', value: 'refs/heads/' + params.BRANCH), string(name: 'VNFM_DUMMY_AMQP', value: 'refs/heads/' + params.BRANCH), string(name: 'PLUGIN_VIMDRIVER_TEST', value: 'refs/heads/' + params.BRANCH), string(name: 'PLUGIN_VIMDRIVER_OPENSTACK', value: 'refs/heads/' + params.BRANCH), string(name: 'INTEGRATION_TESTS', value: 'refs/heads/' + params.BRANCH)]
                    }
                }
            }
        }
        stage('Setup') {
            steps {
                script {
                    echo 'Creating tenant and assigning role'
                    echo '#TODO'
                }
                script {
                    sh 'rm -rf */||true'
                    if (params.SYSTEM_UNDER_TEST != 'standalone') {
                        git branch: 'develop', url: 'https://github.com/openbaton/bootstrap.git'
                        dir('distributions/docker/compose') {
                            if (params.BRANCH != 'master' && params.BRANCH != 'develop') {
                                sh "sed -i 's/latest/${params.BRANCH}/g' ${params.SYSTEM_UNDER_TEST}.yml"
                            }
                            sh "env HOST_IP=$HOST_IP docker-compose -p $BUILD_NUMBER -f ${params.SYSTEM_UNDER_TEST}.yml up -d"
                        }
                    } else {
                        sh "docker run --rm -d -h openbaton-rabbitmq -p 8080:8080 -p 5672:5672 -p 15672:15672 -p 8443:8443 -e RABBITMQ_BROKERIP=$HOST_IP --name=openbaton-standalone openbaton/standalone:latest"
                    }
                }
                sh "timeout 600 bash -c 'until curl -sSf http://$HOST_IP:8080; do sleep 10;done'"
                sleep 20
            }
        }
        stage('Test generic') {
            when { expression { params.VNFM_TO_TEST == 'generic' || params.VNFM_TO_TEST == 'all' } }
            steps {
                script {
                    if (params.SYSTEM_UNDER_TEST != 'standalone') {
                        dir('distributions/docker/compose') {
                            sh "docker-compose -p $BUILD_NUMBER -f ${params.SYSTEM_UNDER_TEST}.yml restart vnfm-generic"
                            sleep 10
                            if (params.BRANCH == 'local') {
                                build job: 'test-generic', parameters: [string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'VIM_LOCATION', value: params.VIM_LOCATION), string(name: 'BRANCH', value: 'local')]
                            } else if (params.BRANCH == 'master' || params.BRANCH == 'develop') {
                                build job: 'test-generic', parameters: [string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'VIM_LOCATION', value: params.VIM_LOCATION), string(name: 'BRANCH', value: 'latest')]
                            } else {
                                build job: 'test-generic', parameters: [string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'VIM_LOCATION', value: params.VIM_LOCATION), string(name: 'BRANCH', value: params.BRANCH)]
                            }
                        }
                    } else {
                        build job: 'test-generic', parameters: [string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'VIM_LOCATION', value: params.VIM_LOCATION), string(name: 'BRANCH', value: 'latest')]
                    }
                }
            }
        }
        stage('Test dummy-amqp') {
            when { expression { params.SYSTEM_UNDER_TEST != 'standalone' && (params.VNFM_TO_TEST == 'dummy-amqp' || params.VNFM_TO_TEST == 'all') } }
            steps {
                script {
                    tag = (params.BRANCH == 'master' || params.BRANCH == 'develop') ? 'latest' : params.BRANCH 
                }
                build job: 'test-dummy', parameters: [string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'BRANCH', value: tag)]
            }
        }
    }
    post {
        always {
            sh 'rm -rf *-log *.log || true'
            script {
                if (params.SYSTEM_UNDER_TEST != 'standalone') {
                    dir('distributions/docker/compose') {
                        sh "for container in \$(docker-compose -p $BUILD_NUMBER -f ${params.SYSTEM_UNDER_TEST}.yml ps|grep $BUILD_NUMBER|awk '{print \$1}');do docker logs \$container > ../../../\$container.log 2>&1;done"
                        sh "docker-compose -p $BUILD_NUMBER -f ${params.SYSTEM_UNDER_TEST}.yml down -v"
                    }
                }
                else {
                    sh "docker cp openbaton-standalone:/var/log/openbaton ./standalone-log"
                    sh "docker stop openbaton-standalone"
                }
            }
            archive '*-log/*.log'
            archive '*.log'
            script {
                echo 'Purging tenant'
                echo '#TODO'
            }
        }
    }
}
