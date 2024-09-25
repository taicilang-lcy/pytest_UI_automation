pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'auto-test-image'  // Docker 镜像名称
        ECS_IP = '8.149.129.172'          // 阿里云 ECS 的 IP 地址
        SSH_CREDENTIALS = 'ecs-ssh-credentials' // Jenkins 中设置的 SSH 凭据 ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                // 从 GitHub 仓库克隆代码，使用 HTTPS 方式
                git branch: 'main', url: 'https://github.com/taicilang-lcy/Automation_Test.git', credentialsId: 'github-automation-test-token'
            }
        }

        stage('Build Docker Image on ECS') {
            steps {
                // SSH 到阿里云 ECS，并在远程服务器上构建 Docker 容器
                script {
                    sshagent([SSH_CREDENTIALS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@${ECS_IP} '
                            cd /usr/automation_pipeline/automation_test && 
                            /usr/bin/git pull && 
                            docker build -t ${DOCKER_IMAGE} .'
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
                        ssh -o StrictHostKeyChecking=no root@${ECS_IP} 'docker run ${DOCKER_IMAGE} pytest tests/'
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
