#!/bin/bash
# Automatización de despliegue para instancia AWS EC2 (Ubuntu)

echo "Iniciando configuración del servidor B2B en AWS EC2..."

# 1. Actualizar dependencias del servidor
sudo apt update -y

# 2. Instalar Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# 3. Construir la imagen del modelo predictivo (Churn API)
sudo docker build -t b2b-churn-api .

# 4. Ejecutar el contenedor en segundo plano, mapeando el puerto 80 al 8000 de FastAPI
sudo docker run -d -p 80:8000 b2b-churn-api

echo "Despliegue finalizado. API operativa en el puerto 80."