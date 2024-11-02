# Based on Adafruit_CircuitPython_DHT Library Example
import os
import requests
import time
import yaml
import board
import adafruit_dht
from adafruit_bme280 import basic as adafruit_bme280
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

with open("conf.yaml") as f:
    conf = yaml.load(f, Loader=yaml.FullLoader)
conf 

def get_aemet_sea_pressure(k_token, station):

    url = f'https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{station}?api_key={k_token}'

    # Make the request to the AEMET API
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()

    # Get the actual data URL from the response
    data_url = data['datos']

    # Fetch the actual data
    data_response = requests.get(data_url)
    if data_response.status_code != 200:
        return None
    weather_data = data_response.json()

    observation = weather_data[-1]  # last
    return observation['pres_nmar']



# Sensor data pin is connected to GPIO 4
# sensor = adafruit_dht.DHT22(board.D4)
# Uncomment for DHT11
sensor = adafruit_dht.DHT11(board.D4)

# connect BME280
i2c = board.I2C()   # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# AEMET apikey
aemet_api = conf["aemet_api"]   # token from aemet
station = "0076"  # estacion aeroport
counter_hora = 1
# URL for the specific station in Barcelona
url = f'https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{station}?api_key={aemet_api}'
# "pres_nmar"

# InfluxDB settings
bucket = "mydatabase"
bucket_bme280 = "bme280"
org = "myorg"

token =  "c8q9oeAZX8IZumbJhPNMS-bsbqKO_aQFpPVAHbwcXHZzuiyzF-8CGyC4mCdBZ-NIg-epq8mZOhlbouTlDCtpgA=="  #  os.environ.get("INFLUXDB_TOKEN")  # token 
url = "http://influxdb:8086" # "http://192.168.1.34:8086/"  # "http://influxdb:8086"

# Create InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        # Read the values from the sensor
        temperature_c = sensor.temperature
        # temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity

        print(temperature_c, humidity)

        # Create a point and write it to the database
        point = Point("sensor_data_router") \
            .tag("sensor_location","wifi_room") \
            .field("temperature_c", temperature_c) \
            .field("humidity", humidity) # \
            # .time(time.time()) , WritePrecision.NS)

        write_api.write(bucket=bucket, org=org, record=point)

        # change this to match the location's pressure (hPa) at sea level
        try:
            if counter_hora%60==0:  # medir de aemet una vez a la hora  por si hay limitaciones
                sea_level_pressure = get_aemet_sea_pressure(aemet_api, station)
                if sea_level_pressure is not None:
                    bme280.sea_level_pressure = sea_level_pressure
                counter_hora = 1
            else:
                counter_hora += 1
        except Exception as e:
            print(f"Exception on AEMET API: {e}")

         # Create a point and write it to the database
        point_280 = Point("sensor_data_router") \
            .tag("sensor_location","wifi_room") \
            .field("temperature_c", round(bme280.temperature, 2)) \
            .field("humidity", round(bme280.relative_humidity, 2)) \
            .field("pressure", round(bme280.pressure, 2)) \
            .field("altitude", round(bme280.altitude, 2)) \
            .field("sea_pressure", round(bme280.sea_level_pressure, 2))
            # .time(time.time()) , WritePrecision.NS)

        write_api.write(bucket=bucket_bme280, org=org, record=point_280)       

        # Wait before taking the next reading
        time.sleep(60.0)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print("Runtime: ", error.args)
        time.sleep(2.0)
        continue
    except Exception as error:
        # raise error
        print( "Exception: ",error.args)
        time.sleep(2)
 
sensor.exit()
client.close()


"""
query_api = client.query_api()

query = '''from(bucket: "test_bucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")'''
tables = query_api.query(query, org="myorg")

for table in tables:
  for record in table.records:
    print(record)
"""
