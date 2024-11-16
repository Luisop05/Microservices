FROM jenkins/jenkins:lts

# Cambiar a usuario root para realizar la instalación
USER root

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Agregar la clave GPG para el repositorio de Docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

# Establecer el repositorio de Docker
RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list

# Actualizar el repositorio e instalar Docker
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io && apt-get clean

# Instalar Docker Compose (versión estática recomendada)
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Volver al usuario jenkins
USER jenkins