FROM jenkins/jenkins:lts

USER root

# Actualizar el sistema e instalar dependencias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Agregar la clave GPG y el repositorio de Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable"

# Actualizar de nuevo el repositorio e instalar Docker y Docker Compose
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins