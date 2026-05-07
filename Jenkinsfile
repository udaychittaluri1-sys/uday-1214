pipeline {
    agent any

    parameters {

        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Browser for UI tests'
        )

        choice(
            name: 'ENV',
            choices: ['dev', 'staging', 'production'],
            description: 'Target environment'
        )

        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )

        string(
            name: 'PARALLEL_WORKERS',
            defaultValue: '4',
            description: 'Number of parallel workers'
        )
    }

    environment {

        TEST_ENV = "${params.ENV}"
        TEST_BROWSER = "${params.BROWSER}"
        HEADLESS_MODE = "${params.HEADLESS}"
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        // ============================================
        // Checkout Source Code
        // ============================================

        stage('Checkout') {

            steps {

                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/udaychittaluri1-sys/uday-1214.git'
                    ]]
                ])

                echo "Repository checked out successfully"
            }
        }

        // ============================================
        // Setup Python Virtual Environment
        // ============================================

        stage('Setup Environment') {

            steps {

                script {

                    if (isUnix()) {

                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate

                            python -m pip install --upgrade pip

                            pip install -r requirements.txt
                        '''

                    } else {

                        bat '''
                            python -m venv venv

                            call venv\\Scripts\\activate

                            python -m pip install --upgrade pip

                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        // ============================================
        // Verify Pytest & Allure
        // ============================================

        stage('Verify Tools') {

            steps {

                script {

                    if (isUnix()) {

                        sh '''
                            . venv/bin/activate

                            pytest --version

                            allure --version || true
                        '''

                    } else {

                        bat '''
                            call venv\\Scripts\\activate

                            pytest --version

                            allure --version
                        '''
                    }
                }
            }
        }

        // ============================================
        // API Health Check
        // ============================================

        stage('API Health Check') {

            steps {

                script {

                    if (isUnix()) {

                        sh '''
                            . venv/bin/activate

                            python -c "import requests; r=requests.get('https://practice.expandtesting.com/notes/api/health-check'); print('API Status:', r.status_code)"
                        '''

                    } else {

                        bat '''
                            call venv\\Scripts\\activate

                            python -c "import requests; r=requests.get('https://practice.expandtesting.com/notes/api/health-check'); print('API Status:', r.status_code)"
                        '''
                    }
                }
            }
        }

        // ============================================
        // Run Pytest Automation
        // ============================================

        stage('Run Tests') {

            steps {

                script {

                    if (isUnix()) {

                        sh """
                            . venv/bin/activate

                            pytest tests/ \
                            -v \
                            -n ${params.PARALLEL_WORKERS} \
                            --reruns 2 \
                            --reruns-delay 2 \
                            --junitxml=reports/results.xml \
                            --alluredir=reports/allure-results
                        """

                    } else {

                        bat """
                            call venv\\Scripts\\activate

                            pytest tests/ ^
                            -v ^
                            -n ${params.PARALLEL_WORKERS} ^
                            --reruns 2 ^
                            --reruns-delay 2 ^
                            --junitxml=reports\\results.xml ^
                            --alluredir=reports\\allure-results
                        """
                    }
                }
            }
        }

        // ============================================
        // Generate Allure Report
        // ============================================

        stage('Generate Allure Report') {

            steps {

                allure(
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']]
                )
            }
        }
    }

    // ============================================
    // Post Actions
    // ============================================

    post {

        always {

            echo 'Publishing reports...'

            junit(
                testResults: 'reports/results.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true
            )
        }

        success {

            echo 'SUCCESS: All tests passed successfully!'
        }

        failure {

            echo 'FAILURE: Some tests failed. Check Allure report.'
        }

        cleanup {

            cleanWs()
        }
    }
}
