FROM jenkins/jenkins:lts

# Cambiar a usuario root para instalar
USER root

# Actualizar el sistema e instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Docker usando el script de instalación
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Instalar Docker Compose (versión estática recomendada)
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Crear grupo docker y añadir usuario jenkins
RUN groupadd -f docker && \
    usermod -aG docker jenkins && \
    chown root:docker /var/run/docker.sock

# Configurar permisos correctos para el socket de Docker
RUN chmod 666 /var/run/docker.sock

# Volver al usuario jenkins
USER jenkins