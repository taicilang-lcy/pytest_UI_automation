pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pytest-image-slim'  // pytest slim 镜像名称
        ECS_IP = '8.149.129.172'              // 阿里云 ECS 的 IP 地址
        SSH_CREDENTIALS = 'ecs-ssh-credentials' // Jenkins 中设置的 SSH 凭据 ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                // 从 GitHub 仓库克隆代码，使用 HTTPS 方式
                git branch: 'main', url: 'https://github.com/taicilang-lcy/pytest_UI_automation.git', credentialsId: 'github-automation-test-token'
            }
        }

        stage('Update Code on ECS') {
            steps {
                script {
                    sshagent([SSH_CREDENTIALS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@${ECS_IP} '
                            cd /usr/automation_pipeline/pytest_UI_automation &&
                            /usr/bin/git pull
                        '
                        """
                    }
                }
            }
        }

        stage('Build Docker Image on ECS') {
            steps {
                script {
                    sshagent([SSH_CREDENTIALS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@${ECS_IP} '
                            cd /usr/automation_pipeline/pytest_UI_automation &&
                            if [[ \$(docker images -q ${DOCKER_IMAGE}) == "" ]]; then
                                echo "Building new Docker image ${DOCKER_IMAGE}..."
                                docker build -t ${DOCKER_IMAGE} .
                            else
                                echo "Using existing image ${DOCKER_IMAGE}"
                            fi
                        '
                        """
                    }
                }
            }
        }

        stage('Run Tests in Docker on ECS') {
            steps {
                script {
                    sshagent([SSH_CREDENTIALS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@${ECS_IP} '
                            echo "Running tests using Docker image ${DOCKER_IMAGE}..."
                            docker run -v /usr/automation_pipeline/pytest_UI_automation:/pytest_UI_automation ${DOCKER_IMAGE} pytest --alluredir=/pytest_UI_automation/report/ test_suites/
                        '
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() // 清理工作区
        }
        success {
            echo 'Tests ran successfully!' // 成功消息
        }
        failure {
            echo 'Build or tests failed.' // 失败消息
        }
    }
}
