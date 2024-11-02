# Sensing at home
Proyecto para crear una estación de medidas ambientales en casa.

El proyecto se plantea a partir de varios contenedores en docker-compose, para ello se consideran los siguientes containers:
- influxdb: Base de datos de series temporales.
- sensor_app: Aquí se desarrollará la aplicación de medición en python para la raspberry pi.
- Grafana: Por ahora es incluye en el docker compose, pero el influxdb ya contiene su propio dashboard.


Sensores actuales:
- DTH11: [VMA311 data sheet](https://cdn.velleman.eu/downloads/29/vma311_a4v01.pdf)
- BME268: [adafruit library info](https://docs.circuitpython.org/projects/bme280/en/latest/)


Steps to configure the data:
- add static ip: https://raspberrytips.com/set-static-ip-address-raspberry-pi/
- find your external ip: https://whatismyipaddress.com/
            para influx: 79.155.75.22:959