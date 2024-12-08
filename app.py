import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from big_mart_sales.exception.exception import BigMartSalesException
from big_mart_sales.logging.logger import logging
from big_mart_sales.pipeline.training_predicition import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from big_mart_sales.utils.main_utils.utils import load_object

from big_mart_sales.utils.ml_utils.model.estimator import BigMartModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from big_mart_sales.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from big_mart_sales.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise BigMartSalesException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        #print(df)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        big_mart_model = BigMartModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = big_mart_model.predict(df)
        print(y_pred)
        df['Item_Outlet_Sales'] = y_pred
        
        data=df[['Item_Identifier','Outlet_Identifier','Item_Outlet_Sales']]
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        data.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise BigMartSalesException(e,sys)
    

    
if __name__=="__main__":
    app_run(app,host="localhost",port=8000)