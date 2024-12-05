from big_mart_sales.components.data_ingestion import DataIngestion
from big_mart_sales.components.data_validation import DataValidation
from big_mart_sales.components.data_transformation import DataTransformation
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging
from big_mart_sales.entity.config_entity import DataIngestionConfig , DataValidationconfig ,DataTransformationconfig
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
        logging.info('Data Ingestion is completed')
        data_validation_config=DataValidationconfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info('Initiating data ingestion')
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info('Data validation completed')
        print(data_validation_artifacts)
        data_transformation_config=DataTransformationconfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
        logging.info('Initiating data transformation')
        data_transformation_artifacts=data_transformation.initiate_data_transformation()

        logging.info('Data transformation completed')
        print(data_transformation_artifacts)

        
    except Exception as e:
        raise BigMartSalesException(e,sys)
