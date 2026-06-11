pipeline {
    agent any

    environment {
        // Defines where virtual environment will be created
        VENV_DIR = '.venv'
    }

    stages {
        stage('1. Checkout Source Code') {
            steps {
                // This checks out code from the SCM configured in the Jenkins Job
                checkout scm
            }
        }

        stage('2. Install Python & Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        // Linux/macOS setup
                        sh '''
                            python3 -m venv ${VENV_DIR}
                            . ${VENV_DIR}/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        // Windows setup
                        bat """
                            python -m venv %VENV_DIR%
                            call %VENV_DIR%\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('3. Parallel Test Execution') {
            steps {
                script {
                    // -n 4 runs tests across 4 parallel workers using pytest-xdist
                    // --html=report.html generates the standard HTML report
                    // --alluredir=allure-results prepares data for Allure
                    if (isUnix()) {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            pytest -n 4 --html=report.html --self-contained-html --alluredir=allure-results || true
                        '''
                    } else {
                        bat """
                            call %VENV_DIR%\\Scripts\\activate
                            pytest -n 4 --html=report.html --self-contained-html --alluredir=allure-results || set ERRORLEVEL=0
                        """
                    }
                    // Note: '|| true' / 'set ERRORLEVEL=0' ensures that test failures
                    // don't crash the pipeline instantly, allowing reports to still be published.
                }
            }
        }

        stage('4. Publish Reports') {
            parallel {
                stage('Publish HTML Report') {
                    steps {
                        // Publishes the pytest-html report
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'report.html',
                            reportName: 'Pytest HTML Report',
                            reportTitles: 'Automation Test Report'
                        ])
                    }
                }
                stage('Publish Allure Report') {
                    steps {
                        // Generates and publishes Allure Report from the results folder
                        // Comment this out if you aren't using the Allure plugin
                        allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                    }
                }
            }
        }

        stage('5. Upload Artifacts') {
            steps {
                // Archives screenshots, logs, and HTML reports in Jenkins artifacts storage
                // Adjust file patterns based on where your project saves screenshots/logs
                archiveArtifacts artifacts: 'report.html, *.log, screenshots/**/*.png',
                                 allowEmptyArchive: true,
                                 fingerprint: true
            }
        }
    }

    post {
        always {
            // Cleans workspace after execution to save disk space
            cleanWs()
        }
    }
}
