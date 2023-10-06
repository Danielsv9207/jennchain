# Usar una imagen base de Python
FROM python:3.8

# Establecer un directorio de trabajo
WORKDIR /usr/src/app

# Copiar los requisitos de tu proyecto
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de tu proyecto
COPY . .

# Exponer el puerto que usa Flask
EXPOSE 8000

# Comando para ejecutar tu aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]