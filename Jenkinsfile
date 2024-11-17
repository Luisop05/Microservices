pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml' // Archivo de configuración de Docker Compose
        GIT_REPO_URL = 'https://github.com/Luisop05/Microservices.git'
        GIT_BRANCH = 'main' // Cambia esto por la rama que deseas clonar, si es diferente
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                script {
                    // Clona el repositorio especificando la rama
                    git branch: "${GIT_BRANCH}", url: "${GIT_REPO_URL}"
                }
            }
        }

        stage('Construir Microservicios') {
            steps {
                script {
                    echo 'Construyendo los microservicios...'
                    // Construir las imágenes de Docker usando docker-compose
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans pedidos-api inventario-api"
                }
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                script {
                    echo 'Ejecutando pruebas...'
                    // Ejecutar pruebas para pedidos-api
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} run pedidos-api python -m unittest discover -s tests"
                    // Ejecutar pruebas para inventario-api
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} run inventario-api python -m unittest discover -s tests"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Iniciando solo los servicios detenidos...'
                    // Iniciar solo los servicios pedidos-api e inventario-api en segundo plano
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans pedidos-api inventario-api"
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
