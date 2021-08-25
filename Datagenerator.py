import json
from pprint import pprint
import random
import time
import boto3
import datetime
import uuid
import string
import pandas as pd
from faker import Faker
fake = Faker()

STREAM_NAME = "tf-teraform-kinesis-kinesis-stream"


def get_data():
    return {
        'EVENT_TIME': datetime.datetime.now().isoformat(),
        'Model': random.choice(['VW', 'PORSCHE', 'BMW', 'AUDI', 'MERCEDES']),
        'speed': str(random.randint(10,200)),
        'record_id': fake.uuid4(),
        'lat':str(fake.latitude()),
        'lon':str(fake.longitude()),
        'vin':''.join([random.choice(string.ascii_letters + string.digits) for n in range(17)])}



def generate(stream_name, kinesis_client):
    max_try = 150
    df = pd.DataFrame()
    while max_try >0:
        data = get_data()
        df = df.append(data,ignore_index=True)
        #print("Data:",data)
        #print(json.dumps(data))
        payload = " ".join(str(value) for value in data.values())
        print(payload)
        #kinesis_client.put_record(StreamName=stream_name, Data=json.dumps(data),PartitionKey="partitionkey")
        kinesis_client.put_record(StreamName=stream_name, Data= payload + "\n",PartitionKey="partitionkey")
        max_try -= 1
    #return df

if __name__ == "__main__":
    generate(STREAM_NAME, boto3.client('kinesis', aws_access_key_id="AKIAXTGPPSMJDY5VHTHC",
    aws_secret_access_key="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",region_name = "eu-central-1"))
    #df.to_excel('Vehicledata.xlsx')

  