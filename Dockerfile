# 1. Usar una imagen oficial de Python ligera para optimizar costos en AWS
FROM python:3.10-slim

# 2. Establecer el directorio de trabajo en el servidor
WORKDIR /app

# 3. Copiar los requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el código de la aplicación (src y los modelos .joblib)
COPY . .

# 5. Exponer el puerto para consumo B2B
EXPOSE 8000

# 6. Comando para arrancar FastAPI con Uvicorn en producción
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]