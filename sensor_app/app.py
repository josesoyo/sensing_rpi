# Based on Adafruit_CircuitPython_DHT Library Example
import os
import time
import board
import adafruit_dht
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Sensor data pin is connected to GPIO 4
# sensor = adafruit_dht.DHT22(board.D4)
# Uncomment for DHT11
sensor = adafruit_dht.DHT11(board.D4)

# InfluxDB settings
bucket = "mydatabase"
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