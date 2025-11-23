# 1. Imagen base: Usamos una versión ligera de Python 3.11
FROM python:3.11-slim

# 2. Directorio de trabajo: Creamos una carpeta 'app' dentro del contenedor
WORKDIR /app

# 3. Copiar dependencias: Pasamos el requirements.txt al contenedor
COPY requirements.txt .

# 4. Instalar dependencias: El contenedor descarga las librerías
# --no-cache-dir ayuda a mantener el contenedor ligero
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código: Pasamos tu app.py y el resto de archivos
COPY . .

# 6. Exponer el puerto: Streamlit usa el 8501 por defecto
EXPOSE 8501

# 7. Comando de inicio: Qué hace el contenedor al encenderse
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
