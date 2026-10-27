pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Attendance System v1'
                echo 'Jenkins pipeline started successfully!'
            }
        }

        stage('Build') {
            steps {
                bat 'docker --version'
                bat 'docker image inspect attendance-system:v1'
            }
        }

        stage('Verify Docker Hub Image') {
            steps {
                bat 'docker image inspect sharmila1327/attendancesystem:v1'
            }
        }
    }
}
