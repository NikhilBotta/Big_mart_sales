import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import os
import sys
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder , StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split
from big_mart_sales.constant.training_pipeline import TARGET_COLUMN
from big_mart_sales.constant.training_pipeline import (DATA_TRANSFORMATION_IMPUTER_PARAMS, DATA_TRANSFORMATION_CATEGORICAL_IMPUTER,
                                                       DATA_TRANSFORMATION_NUMERICAL_COLS,DATA_TRANSFORMATION_ONE_HOT_COLS,
                                                       DATA_TRANSFORMATION_ORDINAL_COLS,DATA_TRANSFORMATION_CATEGORY)

from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging

from big_mart_sales.entity.artifact_entity import (DataValidationArtifacts, DataTransformationArtifacts)
from big_mart_sales.entity.config_entity import DataTransformationconfig

from big_mart_sales.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:DataTransformationconfig):
        try:
            self.data_validation_artifacts=data_validation_artifacts
            self.data_transformation_config =data_transformation_config
        except Exception as e:
            raise BigMartSalesException(e, sys)
    
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise BigMartSalesException(e, sys)
        
    def item_Fat_content(self,data):
        try:
            data['Item_Fat_Content'] = data['Item_Fat_Content'].replace({'low fat': 'Low Fat',
                                                                        'LF': 'Low Fat',
                                                                        'Low fat': 'Low Fat',
                                                                        'reg': 'Regular',
                                                                        'Regular': 'Regular'
                                                                        })
            return data
        except Exception as e:
            raise BigMartSalesException(e, sys)
    
    def get_data_transformer_object(self)->Pipeline:
        try:
            numerical_col=Pipeline(steps=[
            ("imputer",KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)),
            ("standscaler",StandardScaler())
            ])
            #coverting category variables into one-hot and imputing missing values
            one_hot_col = Pipeline(steps=[
            ("imputer",SimpleImputer(strategy="most_frequent")),
            ("one_hot", OneHotEncoder(handle_unknown="ignore", sparse_output=False,drop='first')) ## because we have only 2 outcomes eg:gender male and female 
        
            ])
            #coverting ordinal variables into ordinal and imputing missing values
            ordinal_col = Pipeline(steps=[
            ("imputer",SimpleImputer(strategy="most_frequent")),
            ("ordinal", OrdinalEncoder(categories=DATA_TRANSFORMATION_CATEGORY))
            ])
        
            pre_processor = (ColumnTransformer(transformers=[
            ("numerical", numerical_col, DATA_TRANSFORMATION_NUMERICAL_COLS),
            ("one-hot", one_hot_col, DATA_TRANSFORMATION_ONE_HOT_COLS),
            ("ordinal", ordinal_col, DATA_TRANSFORMATION_ORDINAL_COLS)
            ],verbose_feature_names_out=False))
            return pre_processor
        except Exception as e:
            raise BigMartSalesException(e, sys)
        
        


    def initiate_data_transformation(self)-> DataTransformationArtifacts:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            train_df = self.item_Fat_content(train_df)
            test_df = self.item_Fat_content(test_df)

            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            ##test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
             

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.data_transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.data_transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)


            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path
            )
            return data_transformation_artifact


            
        except Exception as e:
            raise BigMartSalesException(e,sys)






    