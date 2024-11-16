FROM jenkins/jenkins:lts

# Instalar Docker
USER root
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get install -y docker-compose && \
    apt-get clean

USER jenkins