import os
from datetime import datetime

from sensor.constant.training_pipeline import FILE_NAME, TEST_FILE_NAME, TRAIN_FILE_NAME
from sensor.constant.training_pipeline import (ARTIFACT_DIR, PIPELINE_NAME, DATA_INGESTION_DIR_NAME,
                                               DATA_INGESTION_FEATURE_STORE_DIR, DATA_INGESTION_INGESTED_DIR, DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO, DATA_INGESTION_COLLECTION_NAME)
from sensor.constant.training_pipeline import (DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_VALID_DIR, DATA_VALIDATION_INVALID_DIR, DATA_VALIDATION_DRIFT_REPORT_DIR,
                                               DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

from sensor.constant.training_pipeline import (DATA_TRANSFORMATION_DIR_NAME, DATA_TRANSFORMATION_TRANSFORMED_DIR,
                                               DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_FILE_NAME)

from sensor.constant.training_pipeline import (MODEL_TRAINING_DIR_NAME, MODEL_TRAINING_TRAINED_MODEL_DIR, MODEL_TRAINING_TRAINED_MODEL_NAME,
                                               MODEL_TRAINING_SCORE_THRESHOLD, MODEL_FILE_NAME, MODEL_TRAINING_UNDER_OVER_FITTING_THRESHOLD)

from sensor.constant.training_pipeline import (
    MODEL_EVALUATION_DIR_NAME, MODEL_EVALUATION_IMPROVED_SCORE, MODEL_EVALUATION_REPORT_FILE_NAME)

from sensor.constant.training_pipeline import (
    MODEL_PUSHER_DIR_NAME, MODEL_PUSHER_SAVED_MODEL_DIR)


class TrainingPipelineConfig:

    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp = timestamp
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)


class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)

        self.data_ingestion_featrure_store_dir: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)

        self.train_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)

        self.test_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)

        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)

        self.valid_dir = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_VALID_DIR)

        self.invalid_dir = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_INVALID_DIR)

        self.drift_report_dir = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR)

        self.drift_report_file_path = os.path.join(
            self.drift_report_dir, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)

        self.data_transformation_train_file_path: str = os.path.join(
            self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DIR, TRAIN_FILE_NAME.replace(".csv", ".npy"))

        self.data_transformation_test_file_path: str = os.path.join(self.data_transformation_dir,
                                                                    DATA_TRANSFORMATION_TRANSFORMED_DIR, TEST_FILE_NAME.replace('.csv', ".npy"))

        self.data_transformation_transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_FILE_NAME
        )


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.training_pipeline_config = training_pipeline_config

        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, MODEL_TRAINING_DIR_NAME)

        self.model_training_trained_model_dir: str = os.path.join(
            self.model_trainer_dir, MODEL_TRAINING_TRAINED_MODEL_DIR)

        self.model_training_trained_model_file_path = os.path.join(
            self.model_training_trained_model_dir, MODEL_TRAINING_TRAINED_MODEL_NAME)

        self.model_file_path: str = os.path.join("config", "model.yaml")

        self.model_training_threshold_score: float = MODEL_TRAINING_SCORE_THRESHOLD
        self.model_training_under_over_fitting_threshold: float = MODEL_TRAINING_UNDER_OVER_FITTING_THRESHOLD


class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR_NAME)

        self.model_evaluation_report_file_path = os.path.join(self.model_evaluation_dir,
                                                              MODEL_EVALUATION_REPORT_FILE_NAME)

        self.model_evaluation_improved_score: float = MODEL_EVALUATION_IMPROVED_SCORE


class ModelPusherConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_pusher_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME)

        self.model_pusher_model_file_path: str = os.path.join(self.model_pusher_dir, MODEL_FILE_NAME)

        timestamp=round(datetime.now().timestamp())
        self.saved_model_path: str=os.path.join(MODEL_PUSHER_SAVED_MODEL_DIR,
        f"{timestamp}",
        MODEL_FILE_NAME)
