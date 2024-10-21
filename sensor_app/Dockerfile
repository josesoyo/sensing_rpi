FROM python:3.12

WORKDIR /app
ADD . /app/
# Instala dependencias para Blinka y acceso a GPIO
RUN apt-get update && apt-get install -y \
    python3-dev \
    libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

# Instala RPi.GPIO y las demás dependencias Python
RUN pip install --no-cache-dir RPi.GPIO

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "app.py"]