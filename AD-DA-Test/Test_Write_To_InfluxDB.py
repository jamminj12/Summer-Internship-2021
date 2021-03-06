from datetime import datetime
import os
import time
from time import sleep
import ADS1256
import RPi.GPIO as GPIO

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "88G02Se715xyc9nQUuM4YdMyMVTsMHEJ4lzgkyVYF81YPlsCknKqNildzZWXpArDOQPRl_8cMao2sUIETBksTg=="
org = "saxire"
bucket = "dev_bucket"

client = InfluxDBClient(url="http://glin.saxire.net", token=token)


try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
       
       
# use "while True:" to have continous stream of recorded data

#     for x in range(100): #recording 100 data points
    while True:
        ADC_Value = ADC.ADS1256_GetAll()
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = Point("rPi_Data_Log_Test1")\
          .tag("host", "jesse_greyshock")\
          .field("Potentiometer", ADC_Value[0]*5.0/0x7fffff)\
          .field("Photosensor", ADC_Value[1]*5.0/0x7fffff)\
          .time(datetime.utcnow(), WritePrecision.MS)
        
        write_api.write(bucket, org, point)
#         print(ADC_Value[0]*5.0/0x7fffff)
#         print(ADC_Value[1]*5.0/0x7fffff)
#         print ("\33[9A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()

# write_api.write(bucket, org, sequence)
