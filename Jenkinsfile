#!/usr/bin/env groovy
pipeline {
    parameters {
        string(
            name: 'STANDALONE',
            defaultValue: 'refs/heads/master',
            description: 'Branch or tag, e.g. "refs/heads/<branchName>" or "refs/tags/<tagName>, leave empty to pass'
        )
	string(
            name: 'NFVO',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_GENERIC',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_DOCKER_GO',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'VNFM_DUMMY_AMQP',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_VIMDRIVER_TEST',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_VIMDRIVER_OPENSTACK',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'PLUGIN_VIMDRIVER_DOCKER',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
        string(
            name: 'INTEGRATION_TESTS',
            defaultValue: 'refs/tags/5.0.0',
            description: 'Branch or tag, e.g "refs/heads/<branchName>" or "refs/tags/<tagName>", leave empty to pass'
        )
    }

    options {
        disableConcurrentBuilds()
    }

    agent any

    stages {
        stage('Clean workspace') {
            steps {
                sh 'rm -r */ || true'
            }
        }
        stage('Build images') {
            parallel {
                stage('Build standalone') {
                    when { expression { params.STANDALONE != '' } }
                    steps {
                        script {
                            tag = params.STANDALONE.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('standalone') {
                            checkout([$class: 'GitSCM', branches: [[name: params.STANDALONE]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/bootstrap.git']]])
                            dir('distributions/docker/standalone') {
                                sh "docker build -t openbaton/standalone:$tag ."
                            }
                        }
                    }
                }
                stage('Build nfvo') {
                    when { expression { params.NFVO != '' } }
                    steps {
                        script {
                            tag = params.NFVO.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('nfvo') {
                            checkout([$class: 'GitSCM', branches: [[name: params.NFVO]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/NFVO.git']]])
                            sh "docker build -t openbaton/nfvo:$tag ."
                        }
                    }
                }
                stage('Build vnfm-generic') {
                    when { expression { params.VNFM_GENERIC != ''} }
                    steps {
                        script {
                            tag = params.VNFM_GENERIC.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('vnfm-generic') {
                            checkout([$class: 'GitSCM', branches: [[name: params.VNFM_GENERIC]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/generic-vnfm.git']]])
                            sh "docker build -t openbaton/vnfm-generic:$tag ."
                        }
                    }
                }
                stage('Build vnfm-docker-go') {
                    when { expression { params.VNFM_DOCKER_GO != ''} }
                    steps {
                        script {
                            tag = params.VNFM_GENERIC.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('vnfm-docker-go') {
                            checkout([$class: 'GitSCM', branches: [[name: params.VNFM_GENERIC]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/go-docker-vnfm.git']]])
                            sh "docker build -t openbaton/vnfm-docker-go:$tag ."
                        }
                    }
                }
                stage('Build vnfm-dummy-amqp') {
                    when { expression { params.VNFM_DUMMY_AMQP != ''} }
                    steps {
                        script {
                            tag = params.VNFM_DUMMY_AMQP.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('vnfm-dummy-amqp') {
                            checkout([$class: 'GitSCM', branches: [[name: params.NFVO]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/dummy-vnfm-amqp.git']]])
                            sh "docker build -t openbaton/vnfm-dummy-amqp:$tag ."
                        }
                    }
                }
                stage('Build test-plugin') {
                    when { expression { params.PLUGIN_VIMDRIVER_TEST != ''} }
                    steps {
                        script {
                            tag = params.PLUGIN_VIMDRIVER_TEST.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('test-plugin') {
                            checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_VIMDRIVER_TEST]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/test-plugin.git']]])
                            sh "docker build -t openbaton/plugin-vimdriver-test:$tag ."
                        }
                    }
                }
                stage('Build docker-plugin') {
                    when { expression { params.PLUGIN_VIMDRIVER_TEST != ''} }
                    steps {
                        script {
                            tag = params.PLUGIN_VIMDRIVER_TEST.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('go-plugin') {
                            checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_VIMDRIVER_TEST]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/go-docker-driver.git']]])
                            sh "docker build -t openbaton/driver-docker-go:$tag ."
                        }
                    }
                }
                stage('Build openstack4j-plugin') {
                    when { expression { params.PLUGIN_VIMDRIVER_OPENSTACK != ''} }
                    steps {
                        script {
                            tag = params.PLUGIN_VIMDRIVER_OPENSTACK.tokenize("/").last()
                            tag = (tag == 'master'|| tag == 'develop') ? 'latest' : tag
                        }
                        dir('openstack4j-plugin') {
                            checkout([$class: 'GitSCM', branches: [[name: params.PLUGIN_VIMDRIVER_OPENSTACK]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/openstack4j-plugin.git']]])
                            sh "docker build -t openbaton/plugin-vimdriver-openstack-4j:$tag ."
                        }
                    }
                }
                stage('Build integration-tests') {
                    when { expression { params.INTEGRATION_TESTS != ''} }
                    steps {
                        script {
                            tag = params.INTEGRATION_TESTS.tokenize("/").last()
                            tag = (tag == 'master' || tag == 'develop') ? 'latest' : tag
                        }
                        dir('integration-tests') {
                            checkout([$class: 'GitSCM', branches: [[name: params.INTEGRATION_TESTS]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, parentCredentials: false, recursiveSubmodules: true, reference: '', trackingSubmodules: false]], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/openbaton/integration-tests.git']]])
                            sh "docker build -t openbaton/integration-tests:$tag ."
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Tried building docker containers'
        }
        success {
            echo 'Build successful, removing dangling images'
            sh 'docker rmi $(docker images -f "dangling=true" -q)||true'
        }
        failure {
            echo 'Build failed'
        }
        changed {
            echo 'Build returned to successful'
        }
    }
}
