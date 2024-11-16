FROM jenkins/jenkins:lts

# Cambiar a root para instalar
USER root

# Actualizar el sistema e instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Agregar la clave GPG y el repositorio de Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
   add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

# Instalar Docker y Docker Compose
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose \
    && apt-get clean

# Volver al usuario 'jenkins'
USER jenkins