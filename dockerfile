FROM jenkins/jenkins:lts

# Cambiar a root para realizar la instalación
USER root

# Actualizar el repositorio y las dependencias, y preparar la instalación de Docker
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Volver al usuario jenkins
USER jenkins