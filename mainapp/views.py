from django.http import HttpResponse
from django.shortcuts import render
from .task import test_func, add_numbers
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
import logging
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import pandas as pd
from influxdb_client.client.write_api import WriteType
from datetime import datetime
from .models import User, Item
from .serializer import UserSerializer, ItemSerializer
from django.core.cache import cache


# Create your views here.
def test(request):
    test_func.delay()
    return HttpResponse("Done") 

# def sheet(request):
#     bucket="trade_sheets"

#     write_api = client.write_api(write_options=SYNCHRONOUS)
    
#     for value in range(5):
#     point = (
#         Point("measurement1")
#         .tag("tagname1", "tagvalue1")
#         .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="Antino", record=point)
#     time.sleep(1) # separate points by 1 second

#     return HttpResponse("Done") 


class Stocks:
  def __init__(self,token,url,org,bucket:str):
    self.org = org
    self.bucket = bucket
    self.client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, timeout =10000)
    
  # @classmethod
  # def my_bucket(cls,bucket):
  #   return cls(self.token,url,org,bucket)
  
  def write(self,data_frame,write_option = SYNCHRONOUS): 
    logging.basicConfig(level=logging.DEBUG)
    # print("jjjjjjjjjjjjjjjjjjjjjjjj")  
    write_api = self.client.write_api(write_options=write_option)
    # point = (
    #       Point("tp1")
    #       .tag("tagname1", "tagvalue1")
    #       .field("high", 500)
    #       .field("low",250)
    #       .field("name","nifty")
    #     )
    # print(point)
    write_api.write(bucket=self.bucket, org=self.org, record=data_frame)
    # print(self.bucket, self.org)
    # write_api.write(bucket=self.bucket, org=self.org, record=data_frame, data_frame_measurement_name="tp2",
    #                 data_frame_tag_columns="date")
    write_api.close()
    # print(a)
  
    
  def show(self, range, filter, measurement= None):
    query_api = self.client.query_api()
    
    filters = ""
    for i in filter:
      filters += "\n |> " + i

    ranges = ""
    for i in range:
      ranges += "\n |> " + i
    
    query = f"""from(bucket: "{self.bucket}"){ranges}{filters}"""
    print(query)
    tables = query_api.query(query, org=self.org).to_json()
    
    for table in json.loads(tables):
      print(table)
      
  def delete(self, start, stop, measurement = None,tag = None, timestamp = None):
    delete_api = self.client.delete_api()
    filter = ''
    if measurement: 
      filter+= f'_measurement="{measurement}"'
    if tag:
      filter+= json.dumps(tag)
    if timestamp:
      filter+= f'_time="{timestamp}"'
    delete_api.delete(start, stop, filter, bucket=self.bucket, org=self.org)
  def close(self):
    self.client.close()

def df_to_influxdb( df, measurement):
    points = []

    for index, row in df.iterrows():
      
        formatted_date_string = datetime.strptime(str(row['date']), "%Y%m%d").strftime("%Y-%m-%d")
        datetime_string = f"{formatted_date_string} {row['time']}"

        # Convert the combined string to a datetime object
        
        datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        point = {
            "measurement": measurement,
            "tags": {},
            "time": datetime_object,  # Adjust this according to your CSV
            "fields": {}
        }
        point = (
          Point(measurement)
          .tag("datetime", datetime_object)
        )

        for col in df.columns:
            if col != 'date' or col!= 'time':  # Skip the timestamp column
                point.field(col,row[col])

        points.append(point)

    return points



def tp():
    mydata = pd.read_csv("file:///home/antino/Downloads/combined_AARTIIND.csv")
    token = "ojfHkjU8N3jgHIhpoiF9GMTIaQ1lJWKMwYfIXZbtAvNO3zZG8Ke7P6FvrBRDNzGULN3vE2xgdj8kB_0unGU2hw=="
    org = "antino"
    url = "http://localhost:8086"
    bucket="stocks"


    startTime = datetime.now()
    points = df_to_influxdb(mydata,"tp2")
    print()
    print(f'Import finished in: {datetime.now() - startTime}')
    print()
    # print(points)
    #intialize stocks class
    stocks = Stocks(token,url,org,bucket)

#write Records
    print("Want to write records")
    i = input()


    if i in ['y',"Y"]: 
        startTime = datetime.now()
        try:
            stocks.write(data_frame=points,write_option=WriteOptions(write_type=WriteType.batching, batch_size=10_000, flush_interval=1_000))
        except Exception as e:
            print(f"Error: {e}")

        # stocks.show(range=['range(start: -10m)'], filter=['filter(fn: (r) => r._measurement == "tp")'])
        print()
        print(f'Import finished in: {datetime.now() - startTime}')
        print()


# Delete records
    print("\n Want to delete records")
    i = input()

    if i in ['y',"Y"]:
        print("hello")
        start = "1970-01-19T00:00:00Z"
        stop = "2023-10-26T00:00:00Z"
        stocks.delete(start=start,stop=stop,measurement="tp2")
        # stocks.show(range=['range(start: -10m)'], filter=['filter(fn: (r) => r._measurement == "tp")'])
        
        print("\n Want to view records")
        i = input().lower()

    if i in 'y':
        stocks.show(range=['range(start: -10m)'], filter=['filter(fn: (r) => r._measurement == "tp2")'])


    stocks.close()


class ListUsers(APIView):

    def get(self, request): 
        model = User.objects.all()
        serializer = UserSerializer(model, many = True)
        
        cached_user_data = cache.get(f"user_data")
        
        if cached_user_data is not None:
          return Response({
            "data": cached_user_data, 
            "message": "users data",
          })
        
        cache.set(f"user_data", serializer.data)

        return Response({
          "data": serializer.data, 
          "message": "users data",
        })

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAdminUser]

  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = UserSerializer(queryset, many = True)
    return Response(serializer.data)


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status

class ReturnItemList(ListModelMixin, GenericAPIView):

  queryset = Item.objects.all() 
  serializer_class = ItemSerializer

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

class CreateItemList(CreateModelMixin, GenericAPIView):

  serializer_class = ItemSerializer
  def post(self, request, *args, **kwargs):
     return self.create(request, *args, **kwargs)

# Retrieve model mixin. 

class ItemRetrieve(GenericAPIView , RetrieveModelMixin):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)    

class ItemDelete(DestroyModelMixin, GenericAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer

  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)