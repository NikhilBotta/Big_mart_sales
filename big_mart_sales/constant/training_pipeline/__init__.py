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





"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME : str ="BigMartSaledata"
DATA_INGESTION_DATABASE_NAME: str = "nikhilbotta"
DATA_INGESTION_DIR_NAME: str ="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTION_DIR:str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2