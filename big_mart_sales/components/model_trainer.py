import os
import sys
import pandas as pd 
import numpy as np
from big_mart_sales.entity.artifact_entity import DataTransformationArtifacts,ModelTrainerArtifact
from big_mart_sales.entity.config_entity import ModelTrainingconfig
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging

from big_mart_sales.utils.ml_utils.model.estimator import BigMartModel
from big_mart_sales.utils.main_utils.utils import save_object,load_object
from big_mart_sales.utils.main_utils.utils import load_numpy_array_data
from big_mart_sales.utils.ml_utils.metric.regression_metric import get_regression_score

from sklearn.ensemble import (
    GradientBoostingRegressor)


class ModelTrainer :
    def __init__(self, model_trainer_config:ModelTrainingconfig,data_transformation_artifact:DataTransformationArtifacts):
        try:
            self.model_trainer_config= model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact
        except Exception as e:
            raise BigMartSalesException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        model=GradientBoostingRegressor(subsample=0.8,n_estimators=250,
                                         min_samples_split=10,
                                         min_samples_leaf=5,         
                                         max_features=None,
                                         max_depth=3,
                                         loss='absolute_error',

                                         learning_rate=0.1)
        
        best_model=model
        best_model.fit(x_train,y_train)
        y_train_pred=best_model.predict(x_train)
        regression_train_metrics=get_regression_score(y_true=y_train,y_pred=y_train_pred)

        y_test_pred=best_model.predict(x_test)
        regression_test_metrics=get_regression_score(y_true=y_test,y_pred=y_test_pred)


        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Bigmart_Model=BigMartModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=BigMartModel)
        #model pusher
        save_object("final_model/model.pkl",best_model)

        ## Model Trainer Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=regression_train_metrics,
                             test_metric_artifact=regression_test_metrics
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


        


    def initiate_model_trainer(self)-> ModelTrainerArtifact:
            try:

                train_file_path = self.data_transformation_artifact.transformed_train_file_path
                test_file_path = self.data_transformation_artifact.transformed_test_file_path

                #loading training array and testing array
                train_arr = load_numpy_array_data(train_file_path)
                test_arr = load_numpy_array_data(test_file_path)

                x_train, y_train, x_test, y_test = (
                    train_arr[:, :-1],
                    train_arr[:, -1],
                    test_arr[:, :-1],
                    test_arr[:, -1],
                    )

                model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
                return model_trainer_artifact




            except Exception as e:
                raise BigMartSalesException(e,sys)
        