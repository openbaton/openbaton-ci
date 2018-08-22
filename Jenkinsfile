#!/usr/bin/env groovy
pipeline {
    parameters {
        string(
            name: 'SDK',
            defaultValue: '',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_SDK',
            defaultValue: '',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_SDK',
            defaultValue: '',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
	      string(
            name: 'NFVO',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_GENERIC',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_DUMMY_AMQP',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_VIMDRIVER_TEST',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_VIMDRIVER_OPENSTACK',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'INTEGRATION_TESTS',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        choice(
            name: 'SYSTEM_UNDER_TEST',
            choices: 'min_nomysql-compose\nmin-compose\ndockervnfm-compose\nfull-compose',
            description: 'System under test to use'
        )
        choice(
            name: 'VNFM_TO_TEST',
            choices: 'all\ngeneric\ndummy-amqp\nnone',
            description: 'Which vnfms to test against'
        )
        string(
            name: 'TEST_SET',
            defaultValue: 'simple',
            description: 'Run only the most "simple" tests, a specific scenario or "all"'
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
        stage('Clean workspace') {
            steps {
                sh 'rm -r */ || true'
            }
        }
        stage('Build nfvo') {
            when { expression { params.NFVO != '' } }
            steps {
                dir('nfvo') {
                    checkout([$class: 'GitSCM', branches: [[name: params.NFVO]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/NFVO.git']]])
                    sh 'docker build . -t openbaton/nfvo:local'
                }
            }
        }
        stage('Build baseimage') {
            when { expression { params.VNFM_SDK != '' || params.PLUGIN_SDK != '' || params.SDK != '' } }
            steps {
                dir('vnfm-sdk') {
                    checkout([$class: 'GitSCM', branches: [[name: params.VNFM_SDK]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/vnfm-sdk.git']]])
                    sh 'rm -rf nfvo client plugin || true'
                    sh 'cp -rf ../nfvo ./'
                    dir('client') {
                        checkout([$class: 'GitSCM', branches: [[name: params.SDK]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/openbaton-client.git']]])
                    }
                    dir('plugin') {
                        checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_SDK]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/plugin-sdk.git']]])
                    }
                    sh 'cp ../Dockerfile Dockerfile'
                    sh 'docker build . -t baseimage:local'
                }
            }
        }
        stage('Build remaining') {
            parallel {
                stage('Build vnfm-generic') {
                    when { expression { params.VNFM_GENERIC != '' } }
                    steps {
                        dir('vnfm-generic') {
                            checkout([$class: 'GitSCM', branches: [[name: params.VNFM_GENERIC]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/generic-vnfm.git']]])
                            script {
                                if (params.VNFM_SDK != '' || params.SDK != '') {
                                    sh "sed -i 's#openjdk:8-jdk#baseimage:local#g' Dockerfile"
                                }
                            }
                            sh 'docker build . -t openbaton/vnfm-generic:local'
                        }
                    }
                }
                stage('Build vnfm-dummy-amqp') {
                    when { expression { params.VNFM_DUMMY_AMQP != '' } }
                    steps {
                        dir('vnfm-dummy-amqp') {
                            checkout([$class: 'GitSCM', branches: [[name: params.VNFM_DUMMY_AMQP]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/dummy-vnfm-amqp.git']]])
                            script {
                                if (params.VNFM_SDK != '' || params.SDK != '') {
                                    sh "sed -i 's#openjdk:8-jdk#baseimage:local#g' Dockerfile"
                                }
                            }
                            sh 'docker build . -t openbaton/vnfm-dummy-amqp:local'
                        }
                    }
                }
                stage('Build plugin-test') {
                    when { expression { params.PLUGIN_VIMDRIVER_TEST != '' } }
                    steps {
                        dir('plugin-test') {
                            checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_VIMDRIVER_TEST]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/test-plugin.git']]])
		                        script {
                                if (params.PLUGIN_SDK != '' ) {
                                    sh "sed -i 's#openjdk:8-jdk#baseimage:local#g' Dockerfile"
                                }
                            }
                            sh 'docker build . -t openbaton/plugin-vimdriver-test:local'
                        }
                    }
                }
                stage('Build plugin-openstack') {
                    when { expression { params.PLUGIN_VIMDRIVER_OPENSTACK != '' } }
                    steps {
                        dir('plugin-openstack') {
                            checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_VIMDRIVER_OPENSTACK]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/openstack4j-plugin.git']]])
                            script {
                                if (params.PLUGIN_SDK != '' ) {
                                    sh "sed -i 's#openjdk:8-jdk#baseimage:local#g' Dockerfile"
                                }
                            }
                            sh 'docker build . -t openbaton/plugin-vimdriver-openstack-4j:local'
                        }
                    }
                }
                stage('Build integration') {
                    when { expression { params.INTEGRATION_TESTS != '' } }
                    steps {
                        dir('integration-tests') {
                            checkout([$class: 'GitSCM', branches: [[name: params.INTEGRATION_TESTS]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/integration-tests.git']]])
                            script {
                                if (params.SDK != '') {
                                    sh "sed -i 's#openjdk:8-jdk#baseimage:local#g' Dockerfile"
                                }
                            }
                            sh 'docker build . -t openbaton/integration-tests:local'
                        }
                    }
                }
            }
        }
        stage('Tag skipped') {
            steps{
                script {
                    if (params.NFVO == '') {
                        sh 'docker tag openbaton/nfvo:latest openbaton/nfvo:local'
                    }
                    if (params.VNFM_GENERIC == '') {
                        sh 'docker tag openbaton/vnfm-generic:latest openbaton/vnfm-generic:local'
                    }
                    if (params.VNFM_DUMMY_AMQP == '') {
                        sh 'docker tag openbaton/vnfm-dummy-amqp:latest openbaton/vnfm-dummy-amqp:local'
                    }
                    if (params.PLUGIN_VIMDRIVER_TEST == '') {
                        sh 'docker tag openbaton/plugin-vimdriver-test:latest openbaton/plugin-vimdriver-test:local'
                    }
                    if (params.PLUGIN_VIMDRIVER_OPENSTACK == '') {
                        sh 'docker tag openbaton/plugin-vimdriver-openstack-4j:latest openbaton/plugin-vimdriver-openstack-4j:local'
                    }
                    if (params.INTEGRATION_TESTS == '') {
                        sh 'docker tag openbaton/integration-tests:latest openbaton/integration-tests:local'
                    }
                }
            }
        }
        stage('Run tests') {
            when { expression { params.VNFM_TO_TEST != 'none' } }
            steps {
                build job: 'test-main', parameters: [string(name: 'SYSTEM_UNDER_TEST', value: params.SYSTEM_UNDER_TEST), string(name: 'BRANCH', value: 'local'), booleanParam(name: 'TRIGGER_BUILD', value: false), string(name: 'TEST_SET', value: params.TEST_SET), string(name: 'VNFM_TO_TEST', value: params.VNFM_TO_TEST), string(name: 'VIM_LOCATION', value: params.VIM_LOCATION)]
            }
        }
    }
}
