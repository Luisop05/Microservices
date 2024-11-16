# Usar la imagen base de Jenkins
FROM jenkins/jenkins:lts

# Cambiar a usuario root para la instalación
USER root

# Actualizar el sistema e instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Agregar la clave GPG para el repositorio de Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

# Establecer el repositorio de Docker
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list

# Actualizar el repositorio e instalar Docker y Docker Compose
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Volver al usuario 'jenkins'
USER jenkins