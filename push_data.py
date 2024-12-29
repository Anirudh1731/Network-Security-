import os

import sys
import json

from dotenv import load_dotenv
import pymongo.mongo_client

load_dotenv()

MONGO_DB_URI=os.getenv("MONGO_DB_URI")
print(MONGO_DB_URI)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
#from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def cv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URI,tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    FILE_PATH="Network Data\phisingData.csv"
    DATABASE='Anirudh'
    Collection='NetworkData'
    networks_obj=NetworkDataExtract()
    records=networks_obj.cv_to_json_converter(file_path=FILE_PATH)
    print(records)
    no_of_records=networks_obj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
