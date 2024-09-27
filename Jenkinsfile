pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pytest-image-slim'  // pytest slim 镜像名称
        ECS_IP = '8.149.129.172'              // 阿里云 ECS 的 IP 地址
        SSH_CREDENTIALS = 'ecs-ssh-credentials' // Jenkins 中设置的 SSH 凭据 ID
        RECIPIENT = 'liu_congying@163.com'  // 收件人邮箱
    }

    stages {
        stage('Clone Repository') {
            steps {
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
                            docker run -v /usr/automation_pipeline/pytest_UI_automation:/pytest_UI_automation ${DOCKER_IMAGE} pytest --alluredir=/pytest_UI_automation/report/allure-results test_suites/
                        '
                        """
                    }
                }
            }
        }

        stage('Copy Allure Results') {
            steps {
                script {
                    sshagent([SSH_CREDENTIALS]) {
                        sh """
                        echo "Copying allure results from ECS..."
                        scp -o StrictHostKeyChecking=no -r root@${ECS_IP}:/usr/automation_pipeline/pytest_UI_automation/report/allure-results ${WORKSPACE}/report/
                        """
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    includeProperties: false,
                    results: [[path: 'report/allure-results']]
                ])
            }
        }

        stage('List Allure Results') {
            steps {
                script {
                    sh "ls -l ${WORKSPACE}/report/allure-results"
                }
            }
        }
    }

    post {
        success {
            echo 'Tests ran successfully! & Send an email'
            script {
                emailext(
                    subject: "Jenkins Build Successful: ${currentBuild.fullDisplayName}",
                    body: """<p>Good news! The Jenkins build <b>${env.JOB_NAME}</b> (#${env.BUILD_NUMBER}) succeeded.</p>
                            <p>Check the Allure report: ${env.BUILD_URL}allure/</p>""",
                    mimeType: 'text/html',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                    to: "${RECIPIENT}",
                    from: 'liu_congying@163.com',
                    replyTo: 'liu_congying@163.com',
                    attachmentsPattern: 'report/allure-results/**/*'
                )
            }
        }
        failure {
            echo 'Build or tests failed.& Send an email'
            script {
                emailext(
                    subject: "Jenkins Build Failed: ${currentBuild.fullDisplayName}",
                    body: """<p>Unfortunately, the Jenkins build <b>${env.JOB_NAME}</b> (#${env.BUILD_NUMBER}) failed.</p>
                            <p>Please check the details and take necessary actions.</p>""",
                    mimeType: 'text/html',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                    to: "${RECIPIENT}",
                    from: 'liu_congying@163.com',
                    replyTo: 'liu_congying@163.com',
                    attachmentsPattern: 'report/allure-results/**/*'
                )
            }
        }
        always {
            // 在所有步骤执行完毕后才清理工作区
            echo '清理工作区'
            //cleanWs() // 清理工作区
        }
    }
}
