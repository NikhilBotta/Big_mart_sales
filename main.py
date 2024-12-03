from big_mart_sales.components.data_ingestion import DataIngestion
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging
from big_mart_sales.entity.config_entity import DataIngestionConfig 
from big_mart_sales.entity.config_entity import TrainingPipelineConfig
import sys



if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info('Initiating data ingestion')
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
    except Exception as e:
        raise BigMartSalesException(e,sys)
