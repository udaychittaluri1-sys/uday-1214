pipeline {

    agent any

    environment {

        PYTHON = "C:\\Users\\chitt\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        PYTHONPATH = "${WORKSPACE}"
    }

    parameters {

        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Browser Selection'
        )

        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run in headless mode'
        )

        string(
            name: 'PARALLEL_WORKERS',
            defaultValue: '4',
            description: 'Parallel execution workers'
        )
    }

    stages {

        // ============================================
        // Checkout Repository
        // ============================================

        stage('Checkout') {

            steps {

                git branch: 'main',
                url: 'https://github.com/udaychittaluri1-sys/uday-1214.git'

                echo "Repository cloned successfully"
            }
        }

        // ============================================
        // Setup Python Environment
        // ============================================

        stage('Setup Environment') {

            steps {

                bat """
                    "%PYTHON%" --version

                    "%PYTHON%" -m venv venv

                    call venv\\Scripts\\activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                """
            }
        }

        // ============================================
        // Verify Installed Packages
        // ============================================

        stage('Verify Tools') {

            steps {

                bat """
                    call venv\\Scripts\\activate

                    pytest --version

                    pip list
                """
            }
        }

        // ============================================
        // API Health Check
        // ============================================

        stage('API Health Check') {

            steps {

                bat """
                    call venv\\Scripts\\activate

                    python -c "import requests; r=requests.get('https://practice.expandtesting.com/notes/api/health-check'); print('API Status:', r.status_code)"
                """
            }
        }

        // ============================================
        // Run Automation Tests
        // ============================================

        stage('Run Tests') {

            steps {

                bat """
                    call venv\\Scripts\\activate

                    pytest tests ^
                    -v ^
                    -n %PARALLEL_WORKERS% ^
                    --reruns 2 ^
                    --reruns-delay 2 ^
                    --junitxml=reports\\results.xml ^
                    --alluredir=reports\\allure-results
                """
            }
        }

        // ============================================
        // Generate Allure Report
        // ============================================

        stage('Allure Report') {

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

            junit 'reports/results.xml'

            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true
            )
        }

        success {

            echo 'All tests passed successfully!'
        }

        failure {

            echo 'Tests failed. Check Allure report.'
        }

        cleanup {

            cleanWs()
        }
    }
}
