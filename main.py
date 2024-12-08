from big_mart_sales.components.data_ingestion import DataIngestion
from big_mart_sales.components.data_validation import DataValidation
from big_mart_sales.components.data_transformation import DataTransformation
from big_mart_sales.components.model_trainer import ModelTrainer
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging
from big_mart_sales.entity.config_entity import DataIngestionConfig , DataValidationconfig ,DataTransformationconfig , ModelTrainingconfig
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
        model_train_config=ModelTrainingconfig(trainingpipelineconfig)
        model_trainer =ModelTrainer(data_transformation_artifact=data_transformation_artifacts,model_trainer_config=model_train_config)
        logging.info('Initiating model training')
        model_trainer_artifacts=model_trainer.initiate_model_trainer()
        logging.info('model training completed')

        print(model_trainer_artifacts)

        
    except Exception as e:
        raise BigMartSalesException(e,sys)
