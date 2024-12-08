from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_filed_path : str
    test_filed_path : str


@dataclass
class DataValidationArtifacts:
    validation_status : bool
    valid_train_file_path : str
    valid_test_file_path : str
    invalid_train_file_path : str
    invalid_test_file_path : str
    drift_report_file_path : str


@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str



@dataclass
class RegressionMetricArtifact:
    r2_score: float
    rmse: float
 
    
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: RegressionMetricArtifact
    test_metric_artifact: RegressionMetricArtifact