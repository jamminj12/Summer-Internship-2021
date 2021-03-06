import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "88G02Se715xyc9nQUuM4YdMyMVTsMHEJ4lzgkyVYF81YPlsCknKqNildzZWXpArDOQPRl_8cMao2sUIETBksTg=="
org = "saxire"
bucket = "dev_bucket" # change to write to different bucket

client = InfluxDBClient(url="http://glin.saxire.net", token=token)


"""
    FAILED UPLOADS TO INFLUXDB DUE TO FAULTY
    NETWORK CONNECTION THAT NEED TO BE UPLOADED TO SYSTEM

    RUN SCRIPT TO UPLOAD FILES LISTED IN 'Failed_Uploads_to_InfluxDB.txt'
    
    FILES ERASED FROM LIST ONCE UPLOADED
"""

with open('Failed_Uploads_to_InfluxDB.txt','r+') as f:
    for line in f:
        filename = str(line).rstrip("\n") # (ex. 29-July-2021_13-37-44.csv)
        print(filename)

        file_path = r'/home/pi/Data_Logging/'+filename # if folder name changes for CSV log, make sure to change it here and at the start of the script
        df = pd.read_csv(file_path)
        df['He Flow Avg'] = df.He_Flow_Rate.rolling(window=10).mean()
        df['He Flow Avg'] = df['He Flow Avg'].fillna(0)
                               
        while True:
                                    
            for row_index, row in df.iterrows():
                tag1 = row[1]
                tag2 = row[2]
                tag3 = row[3]
                tag4 = row[4]
                tag5 = row[5]
                fieldValue1 = row[6]
                fieldValue2 = row[7]
                fieldValue3 = row[9]
                write_api = client.write_api(write_options=SYNCHRONOUS)
                json_body = [
                    {
                        "measurement": "TEST5", # change this to write to different measurement grouping
                        "time": row[0],
                        "tags": {
                            "Operator": tag1,
                            "Production Order": tag2,
                            "Material #": tag3,
                            "Quantity": tag4,
                            "Serial #": tag5
                                        },
                        "fields": {
                                "Leak Rate": fieldValue1,
                                "Inlet Pressure": fieldValue2,
                                "Helium Flow": fieldValue3
                        }
                    }
                ]
                write_api.write(bucket,org,json_body)
            break
    f.truncate(0)
print('DONE')