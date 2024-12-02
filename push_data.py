import os
import sys
import json
import certifi
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import pymongo
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging


load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
ca=certifi.where()

class BigMartSaleExtract():
    def __init__(self) :
        try:
            pass
        except Exception as e:
            raise BigMartSalesException(e,sys)
        

    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)  #removing the index
            records= list(json.loads(data.T.to_json()).values())  #extract the values as a list of dictionaries
            return records
        except Exception as e:
            raise BigMartSalesException(e,sys)
    
    def load_data_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection =collection

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database= self.mongo_client[self.database]
            self.collection= self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise BigMartSalesException(e,sys)
        

if __name__=='__main__':
    FILE_PATH="BIG_MART_DATA/train_v9rqX0R.csv"
    DATABASE="nikhilbotta"
    COLLECTION="BigMartSaledata"
    BigMartobj=BigMartSaleExtract()
    records=BigMartobj.csv_to_json(FILE_PATH)
    print(records)
    no_of_records=BigMartobj.load_data_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)

    

    
