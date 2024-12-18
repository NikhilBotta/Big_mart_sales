import sys
import os

from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging

from big_mart_sales.components.data_ingestion import DataIngestion
from big_mart_sales.components.data_validation import DataValidation
from big_mart_sales.components.data_transformation import DataTransformation
from big_mart_sales.components.model_trainer import ModelTrainer

from big_mart_sales.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationconfig,
    DataTransformationconfig,
    ModelTrainingconfig   
)

from big_mart_sales.entity.artifact_entity import(
    DataIngestionArtifacts,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data Ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise BigMartSalesException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts):
        try:
            data_validation_config=DataValidationconfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise BigMartSalesException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifacts):
        try:
            data_transformation_config = DataTransformationconfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise BigMartSalesException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifacts)->ModelTrainerArtifact:
        try:
            self.model_trainer_config: ModelTrainingconfig = ModelTrainingconfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise BigMartSalesException(e, sys)
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise BigMartSalesException(e,sys)