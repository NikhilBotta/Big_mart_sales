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

