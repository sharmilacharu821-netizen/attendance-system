
pipeline {
    agent any

    environment {
        DOCKER = 'C:\\Users\\Sharmila Sivakumar\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE = 'attendance-system'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Attendance System v1 - source checked out'
            }
        }

        stage('Check Docker') {
            steps {
                bat '"%DOCKER%" --version'
            }
        }

        stage('Build Docker Image v1') {
            steps {
                bat '"%DOCKER%" build -t %IMAGE%:v1 .'
            }
        }

        stage('Verify Docker Image v1') {
            steps {
                bat '"%DOCKER%" image inspect %IMAGE%:v1'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Attendance System v1 Docker image built and verified.'
        }
        failure {
            echo 'FAILED: Check Console Output for the exact error.'
        }
    }
}
