from big_mart_sales.entity.artifact_entity import RegressionMetricArtifact
from big_mart_sales.exception.exception import BigMartSalesException
from sklearn.metrics import mean_squared_error,r2_score
import sys
import numpy as np

def rmse(y_true,y_pred):
    return np.sqrt(mean_squared_error(y_true,y_pred))


def get_regression_score(y_true,y_pred)->RegressionMetricArtifact:
    try:
            
        model_rmse_score = rmse(y_true, y_pred)
        model_r2_score = r2_score(y_true, y_pred)
        

        regression_metric =  RegressionMetricArtifact(rmse=model_rmse_score,
                    r2_score=model_r2_score)
                    
        return regression_metric
    except Exception as e:
        raise BigMartSalesException(e,sys)