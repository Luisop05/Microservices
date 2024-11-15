pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // Cambiar al directorio del proyecto de microservicios
                dir('Microservices') {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy') {
            steps {
                // Cambiar al directorio del proyecto de microservicios
                dir('Microservices') {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}