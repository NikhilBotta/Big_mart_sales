from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging
from big_mart_sales.entity.config_entity import DataIngestionConfig #data ingestion config
from big_mart_sales.entity.artifact_entity import DataIngestionArtifacts
import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL= os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise BigMartSalesException(e,sys)
    
    def export_collection_as_dataframe(self):
        '''
        Reading data from mongodb 

        '''
        try:
            
            database_name = self.data_ingestion_config.database_name 
            collection_name= self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
             df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
            
        except Exception as e:
            raise BigMartSalesException(e,sys)
    
    def export_data_into_feature_Store(self,dataframe :pd.DataFrame):
        '''
        Storing raw data in features 
        '''
        try:
            feature_store_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise BigMartSalesException(e,sys)
        
        
    def train_test_split(self,dataframe:pd.DataFrame):
        '''
        Dividing the dataframe into train and test
        '''
        try :
            train_set,test_set =train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42
            )
            logging.info("Performed Train Test Split on dataframe")
            logging.info("Existing split_data_train_test method of Data Ingestion")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.testing_file_path
                            ,index=False,header=True)
            
            logging.info(f"Exported train and test file path.")


        except Exception as e:
            raise BigMartSalesException(e,sys)


    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_Store(dataframe)
            self.train_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifacts(trained_filed_path=self.data_ingestion_config.training_file_path,
                                                         test_filed_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise BigMartSalesException(e,sys)

    
    
    
    
    
    
    
    
    
    
    
    
   