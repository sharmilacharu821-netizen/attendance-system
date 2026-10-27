pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Attendance System v1'
                echo 'Jenkins pipeline started successfully!'
            }
        }

        stage('Check Docker CLI') {
            steps {
                bat '"C:\\Users\\Sharmila Sivakumar\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" --version'
            }
        }

        stage('Verify Attendance Image') {
            steps {
                bat '"C:\\Users\\Sharmila Sivakumar\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" image inspect attendance-system:v1'
            }
        }
    }
}
