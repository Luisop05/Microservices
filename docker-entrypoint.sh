#!/bin/bash

# Configurar permisos del socket de Docker si existe
if [ -e /var/run/docker.sock ]; then
    chown root:docker /var/run/docker.sock
    chmod 666 /var/run/docker.sock
fi

# Ejecutar Jenkins
exec /usr/local/bin/jenkins.sh