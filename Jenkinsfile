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
                    // En Windows, usa checkout de Jenkins o git.exe
                    checkout([
                        $class: 'GitSCM', 
                        branches: [[name: "${GIT_BRANCH}"]], 
                        userRemoteConfigs: [[url: "${GIT_REPO_URL}"]]
                    ])
                }
            }
        }

        stage('Construir Microservicios') {
            steps {
                script {
                    echo 'Construyendo los microservicios...'
                    // Usa docker-compose en Windows
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} build pedidos-api inventario-api"
                }
            }
        }

        stage('Ejecutar Pruebas') {
            steps {
                script {
                    echo 'Ejecutando pruebas...'
                    // Usa bat en lugar de sh para comandos de Windows
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} run pedidos-api python -m unittest discover -s tests"
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} run inventario-api python -m unittest discover -s tests"
                }
            }
        }

        stage('Bajar Contenedores') {
            steps {
                script {
                    echo 'Bajando los contenedores existentes...'
                    // Comandos de Docker Compose para Windows
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} stop pedidos-api"
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} rm -f pedidos-api"
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} stop inventario-api"
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} rm -f inventario-api"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Iniciando solo los servicios detenidos...'
                    // Iniciar servicios en Windows
                    bat "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d pedidos-api inventario-api"
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