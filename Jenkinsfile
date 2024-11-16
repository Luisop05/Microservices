pipeline {
    agent any

    stages {
        stage('Clonar Repositorio') {
            steps {
                git url: 'https://github.com/Luisop05/Microservices.git' 
            }
        }

        stage('Construir Microservicios') {
            steps {
                script {
                    // Construir los microservicios usando docker-compose
                    sh 'docker-compose build'
                }
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                script {
                    sh 'docker-compose run pedidos-api python -m unittest discover -s tests' // Modifica según tu estructura de pruebas
                    sh 'docker-compose run inventario-api python -m unittest discover -s tests' // Modifica según tu estructura de pruebas
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado con éxito!'
        }
        failure {
            echo 'El pipeline ha fallado.'
        }
    }
}
