# Training components of each pipeline is initialized here:

import os
import sys
from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidatoinArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation


class TrainingPipeline:

    # is_pipeline_running = False

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:

            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)

            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(
                f"Data ingestion completed and artifact generated :{data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validataion(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidatoinArtifact:
        try:

            self.data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config)

            logging.info("Starting data validation")
            data_validation = DataValidation(
                data_validation_config=self.data_validation_config, data_ingestion_aritfact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(
                f"Data validation completed and artifact generated :{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)
        try:

            pass

        except Exception as e:
            raise SensorException(e, sys)

    def start_data_transformation(self):
        try:

            pass

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self):
        try:

            pass

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self):
        try:

            pass

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self):
        try:

            pass

        except Exception as e:
            raise SensorException(e, sys)

    def run_pipeline(self):
        try:

            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact: DataValidatoinArtifact = self.start_data_validataion(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise SensorException(e, sys)
