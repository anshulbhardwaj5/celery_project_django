import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "Antino"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# export INFLUXDB_TOKEN=kYLalsEvh5WfK8c-U0AWgfPfLwhIiMVZslqsca-64fWUzgpnFJJoyuR403cGx9hSLuIOZnsX2ghyYHTfYq9U0Q==    