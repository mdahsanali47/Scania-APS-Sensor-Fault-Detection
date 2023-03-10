# Training components of each pipeline is initialized here:

import os
import sys
from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig,
                                         ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig)
from sensor.entity.artifact_entity import (DataIngestionArtifact, DataValidatoinArtifact, DataTransformationArtifact,
                                           ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact)
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.cloud_storage.s3_syncer import S3Sync


class TrainingPipeline:

    is_pipeline_running = False

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()

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

    def start_data_transformation(self, data_validaton_artifact: DataValidatoinArtifact) -> DataTransformationArtifact:
        try:

            self.data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config)

            logging.info("Starting data transformation")
            data_transformation = DataTransformation(
                data_transformation_config=self.data_transformation_config, data_validation_artifact=data_validaton_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(
                f"Data transformation completed and artifact generated :{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:

            self.model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config)

            logging.info("Starting model trainer")
            model_trainer = ModelTrainer(
                model_trainer_config=self.model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(
                f"Model training completed and artifact generated :{model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_evaluation(self, data_validation_artifact: DataValidatoinArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:

            model_evaluation_config = ModelEvaluationConfig(
                training_pipeline_config=self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                               data_validation_artifact=data_validation_artifact,
                                               model_trainer_artifact=model_trainer_artifact)

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:

            model_pusher_config = ModelPusherConfig(
                training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(
                model_pusher_config=model_pusher_config, model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)
            
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_buket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder = SAVED_MODEL_DIR,aws_buket_url=aws_buket_url)
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:

            TrainingPipeline.is_pipeline_running = True

            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            data_validation_artifact: DataValidatoinArtifact = self.start_data_validataion(
                data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact: DataTransformationArtifact = self.start_data_transformation(
                data_validaton_artifact=data_validation_artifact)

            model_trainer_artifact: ModelTrainerArtifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact)

            model_evaluation_artifact: ModelEvaluationArtifact = self.start_model_evaluation(
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)

            model_pusher_artifact = self.start_model_pusher(
                model_evaluation_artifact=model_evaluation_artifact)

            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model is not accepted as trained model is no better than baseline model")

                # raise Exception("Model is not accepted as trained model is no better than baseline model")

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except  Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running=False
            raise SensorException(e, sys)
