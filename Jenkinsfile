pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'pytest-image-slim'  // pytest slim 镜像名称
        ECS_IP = '8.149.129.172'              // 阿里云 ECS 的 IP 地址
        SSH_CREDENTIALS = 'ecs-ssh-credentials' // Jenkins 中设置的 SSH 凭据 ID
        RECIPIENT = 'liu_congying@163.com'  // 收件人邮箱
        BUILD_TIMESTAMP = "${new Date().format('yyyyMMdd_HHmmss')}" // 每次构建的唯一时间戳
        BUILD_RESULTS_DIR = "/usr/automation_pipeline/pytest_UI_automation/report/allure-results-${BUILD_TIMESTAMP}" // ECS 上的结果目录
        BUILD_REPORTS_DIR = "/usr/automation_pipeline/pytest_UI_automation/report/allure-reports-${BUILD_TIMESTAMP}" // ECS 上的报告目录
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/taicilang-lcy/pytest_UI_automation.git', credentialsId: 'Jenkins-lcygithub-ID'
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
                            CONTAINER_NAME=pytest_container_\$(date +%Y%m%d_%H%M%S)
                            docker run --name \${CONTAINER_NAME} -v /usr/automation_pipeline/pytest_UI_automation:/pytest_UI_automation ${DOCKER_IMAGE} pytest -v -s --alluredir=${BUILD_RESULTS_DIR} test_suites/
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
                        scp -o StrictHostKeyChecking=no -r root@${ECS_IP}:${BUILD_RESULTS_DIR}/* ${WORKSPACE}/report/allure-results-${BUILD_TIMESTAMP}/
                        """
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // 生成 Allure 报告到唯一的报告目录
                    sh "allure generate ${WORKSPACE}/report/allure-results-${BUILD_TIMESTAMP} --clean -o ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}"
                }
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    includeProperties: false,
                    results: [[path: "${WORKSPACE}/report/allure-results-${BUILD_TIMESTAMP}"]]
                ])
            }
        }

        stage('List Allure Results') {
            steps {
                script {
                    sh "ls -l ${WORKSPACE}/report/allure-results-${BUILD_TIMESTAMP}"
                }
            }
        }
    }

    post {
        success {
            echo 'Tests ran successfully! & Send an email'
            script {
                // 查看 allure-reports 文件夹的内容
                sh "ls -R ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}"

                // 压缩 allure-reports 文件夹
                sh "zip -r ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}.zip ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}/*"
                emailext(
                    subject: "Jenkins Build Successful: ${currentBuild.fullDisplayName}",
                    body: """<p>Good news! The Jenkins build <b>${env.JOB_NAME}</b> (#${env.BUILD_NUMBER}) succeeded.</p>
                            <p>Check the Allure report: ${env.BUILD_URL}allure/</p>""",
                    mimeType: 'text/html',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                    to: "${RECIPIENT}",
                    from: 'liu_congying@163.com',
                    replyTo: 'liu_congying@163.com',
                    attachmentsPattern: "${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}.zip"  // 指定压缩文件作为附件
                )
            }
            // 清理工作区
            cleanWs() // 清理工作区
        }
        failure {
            echo 'Build or tests failed.& Send an email'
            script {
                // 查看 allure-reports 文件夹的内容
                sh "ls -R ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}"

                // 压缩 allure-reports 文件夹
                sh "zip -r ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}.zip ${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}/*"
                emailext(
                    subject: "Jenkins Build Failed: ${currentBuild.fullDisplayName}",
                    body: """<p>Unfortunately, the Jenkins build <b>${env.JOB_NAME}</b> (#${env.BUILD_NUMBER}) failed.</p>
                            <p>Please check the details and take necessary actions.</p>""",
                    mimeType: 'text/html',
                    recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']],
                    to: "${RECIPIENT}",
                    from: 'liu_congying@163.com',
                    replyTo: 'liu_congying@163.com',
                    attachmentsPattern: "${WORKSPACE}/report/allure-reports-${BUILD_TIMESTAMP}.zip"  // 指定压缩文件作为附件
                )
            }
            // 清理工作区
            cleanWs() // 清理工作区
        }
        always {
            echo '所有步骤执行完毕'
        }
    }
}
