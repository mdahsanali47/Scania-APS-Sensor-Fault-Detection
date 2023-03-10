# Pipeline name and root directory are constants
# that are used in multiple places.

import os

# common constant variables for training pipeline.
TARRGET_COLUMN = "class"
PIPELINE_NAME: str = "sensor"

ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "sensor.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_FILE_NAME: str = "preprocessing.pkl"
MODEL_FILE_NAME: str = "model.pkl"

SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLUMN = "drop_columns"

# constants related to data ingestion:
DATA_INGESTION_COLLECTION_NAME: str = "car"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested_data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# constants related to data validation:
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "drift_report.yaml"

# Data Transformation related constants:
DATA_TRANSFORMATION_DIR_NAME: str = 'data transformation'
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "data transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed object"

# constants related to model training:
MODEL_TRAINING_DIR_NAME: str = "model_trainer"
MODEL_TRAINING_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINING_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINING_SCORE_THRESHOLD: float = 0.75
MODEL_TRAINING_UNDER_OVER_FITTING_THRESHOLD: float = 0.05

# constants related to model evaluation:
MODEL_EVALUATION_DIR_NAME: str = "model_evaluator"
MODEL_EVALUATION_IMPROVED_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_FILE_NAME = "model_evaluation_report.yaml"

SAVED_MODEL_DIR:str = os.path.join('saved_models')

# constants related to model pusher
MODEL_PUSHER_DIR_NAME: str = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR: str = SAVED_MODEL_DIR
