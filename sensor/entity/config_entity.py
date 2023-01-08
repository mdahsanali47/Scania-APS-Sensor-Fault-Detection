import os
from datetime import datetime

from sensor.constant.training_pipeline import FILE_NAME, TEST_FILE_NAME, TRAIN_FILE_NAME
from sensor.constant.training_pipeline import (ARTIFACT_DIR, PIPELINE_NAME, DATA_INGESTION_DIR_NAME,
                                               DATA_INGESTION_FEATURE_STORE_DIR, DATA_INGESTION_INGESTED_DIR, DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO, DATA_INGESTION_COLLECTION_NAME)


class TrainingPipelineConfig:

    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%Y/%m/%d %H:%M:%S")
        self.timestamp = timestamp
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)


class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)

        self.data_ingestion_featrure_store_dir:str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)

        self.train_file_path:str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)

        self.test_file_path:str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)

        self.train_test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str = DATA_INGESTION_COLLECTION_NAME
