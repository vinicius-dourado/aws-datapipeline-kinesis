import json
import urllib.parse
import boto3
import time, urllib
import requests
import pandas as pd
import io
import geopy
from io import StringIO
from geopy.geocoders import Nominatim
import numpy as np
import re

print('Loading function_')

s3 = boto3.client('s3')

geolocator = Nominatim(user_agent="metadata")

#it uses geolocate library to get the location based in coordinates
def city_state_country(row):
    coord_ori = f"{row['lat_ori']}, {row['lon_ori']}"
    coord_dest = f"{row['lat_dest']}, {row['lon_dest']}"
    try:
        location_ori = geolocator.reverse(coord_ori, exactly_one=True)
        location_dest = geolocator.reverse(coord_dest, exactly_one=True)
        address_ori = location_ori.raw['address']
        address_dest = location_dest.raw['address']
        city_ori = address_ori.get('city', '')
        state_ori = address_ori.get('state', '')
        country_ori = address_ori.get('country', '')
        city_dest = address_dest.get('city', '')
        state_dest = address_dest.get('state', '')
        country_dest = address_dest.get('country', '')    
        row['city_ori'] = str(city_ori)
        row['state_ori'] = str(state_ori)
        row['country_ori'] = str(country_ori)
        row['city_dest'] = str(city_dest)
        row['state_dest'] = str(state_dest)
        row['country_dest'] = str(country_dest)
    except:        
        print('not found')
    return row

def convert_time(timedf):
    timetup = time.gmtime(timedf)
    timetup = time.strftime('%Y-%m-%d %H:%M:%S', timetup)
    return timetup

def lambda_handler(event, context):

    # get the location of source and target buckets and their keys
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    print(source_bucket)
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    print(object_key)
    target_bucket = 'trips-presentation-layer-dev'

    # Get the original S3 object using the presigned URL    
    try:
        
        #read json and save it in a dataframe
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=object_key)
        obj = s3.get_object(Bucket=source_bucket, Key=object_key)
        json_df = json.loads(obj['Body'].read())
        json_df=pd.DataFrame(json_df)
        
        #just clean coordinates in order to be used by geolocator library
        json_df.origin_coord = json_df.origin_coord.str.replace('POINT','')
        json_df.origin_coord = json_df.origin_coord.str.replace('(','')
        json_df.origin_coord = json_df.origin_coord.str.replace(')','')
        json_df.origin_coord = json_df.origin_coord.str.replace(',','')
        json_df.origin_coord = json_df.origin_coord.str.lstrip()
        json_df.origin_coord = json_df.origin_coord.str.replace(' ',',') 

        json_df.destination_coord = json_df.destination_coord.str.replace('POINT','')
        json_df.destination_coord = json_df.destination_coord.str.replace('(','')
        json_df.destination_coord = json_df.destination_coord.str.replace(')','')
        json_df.destination_coord = json_df.destination_coord.str.replace(',','')
        json_df.destination_coord = json_df.destination_coord.str.lstrip()
        json_df.destination_coord = json_df.destination_coord.str.replace(' ',',')        

        json_df[['lat_ori', 'lon_ori']] = json_df['origin_coord'].str.split(',', 1, expand=True)
        json_df[['lat_dest', 'lon_dest']] = json_df['destination_coord'].str.split(',', 1, expand=True)

        #apply geolocator library and add 6 new columns (city, state and country for both origin and destination
        #) in the dataframe
        json_df = json_df.apply(city_state_country, axis=1)
        json_df['datetime'] = json_df['datetime'].apply(convert_time)

        service_name = 's3'
        region_name = 'us-east-1'
    
        s3_resource = boto3.resource(
            service_name=service_name,
            region_name=region_name
        )

        #save the new dataframe in a new json file in s3 presentation layer
        csv_buffer = StringIO()
        json_df.to_json(csv_buffer,orient='records')
        s3_resource.Object(target_bucket, object_key).put(Body=csv_buffer.getvalue())
        response = s3.get_object(Bucket=target_bucket, Key=object_key)
        
    except Exception as err:
        print ("Error -"+str(err))
        return err
