from big_mart_sales.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from big_mart_sales.entity.config_entity import DataValidationconfig
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.constant.training_pipeline import SCHEMA_FILE_PATH
from big_mart_sales.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys
from big_mart_sales.utils.main_utils.utils import read_yaml_file , write_yaml_file

class DataValidation :
    def __init__(self,data_ingestion_artifacts: DataIngestionArtifacts,
                 data_validation_config=DataValidationconfig):
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._schema_config= read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise BigMartSalesException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise BigMartSalesException(e,sys)
        

    def validation_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns= len(self._schema_config)
            logging.info(f'Required number of columns :{number_of_columns}')
            logging.info(f'Data frame has columns:{len(dataframe.columns)}')
            if len(dataframe.columns)==number_of_columns:
                return True
            return False 

        except Exception as e:
            raise BigMartSalesException(e,sys)
        

    
        

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) -> bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                sample_dis=ks_2samp(d1,d2)
                if threshold <= sample_dis.pvalue:
                    is_found = False 
                else :
                    is_found = True
                    status = False 
                report.update({column:{"p-value":float(sample_dis.pvalue),
                                       "drift_status":is_found}})
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            #create directory
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise BigMartSalesException(e,sys)


    

    def initiate_data_validation(self)-> DataValidationArtifacts:
        try:
            train_file_path = self.data_ingestion_artifacts.trained_filed_path
            test_file_path = self.data_ingestion_artifacts.test_filed_path
            # read train and test data
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            #validate number of columns
            status=self.validation_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f'Train Data frame does not contain all columns.\n'
            status=self.validation_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f'Test Data frame does not contain all columns.\n'

           

            # check any datadrift 
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False ,header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False ,header=True
            )

            data_validation_artifacts=DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifacts.trained_filed_path,
                valid_test_file_path=self.data_ingestion_artifacts.test_filed_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            return data_validation_artifacts
        





        except Exception as e:
            raise BigMartSalesException(e,sys)




