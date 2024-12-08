import os
import sys
import pandas as pd
import numpy as np

"""
Defining common constant variables
"""
TARGET_COLUMN ="Item_Outlet_Sales"
PIPELINE_NAME: str="BigMartSales"
ARTIFACT_DIR: str="Artifacts"
FILE_NAME : str="train_v9rqX0R.csv"

TRAIN_FILE_NAME : str ="training.csv"
TEST_FILE_NAME : str ="test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"



"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME : str ="BigMartSaledata"
DATA_INGESTION_DATABASE_NAME: str = "nikhilbotta"
DATA_INGESTION_DIR_NAME: str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTION_DIR:str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
Data Validation related constant start with Data_validation VAR NAME
"""

DATA_VALIDATION_DIR_NAME :str = "data_validation"
DATA_VALIDATION_VALID_DIR :str="validated"
DATA_VALIDATION_INVALID_DIR : str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME :str="report.yaml"


"""
Data Transformation related constant start with Data_Transformation VAR NAME
"""

DATA_TRANSFORMATION__DIR_NAME : str ="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR :str ="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR :str ="transformed_object"

## kkn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_CATEGORICAL_IMPUTER = strategy="most_frequent"
DATA_TRANSFORMATION_NUMERICAL_COLS=['Item_Weight','Item_Visibility','Item_MRP','Outlet_Establishment_Year']
DATA_TRANSFORMATION_ONE_HOT_COLS=['Item_Fat_Content','Item_Type','Outlet_Identifier','Outlet_Type']
DATA_TRANSFORMATION_ORDINAL_COLS=['Outlet_Size','Outlet_Location_Type']
DATA_TRANSFORMATION_CATEGORY = [['Small', 'Medium', 'High'],['Tier 3', 'Tier 2','Tier 1']] 


DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

"""
Model training related constant start with Model Training VAR NAME

"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05


