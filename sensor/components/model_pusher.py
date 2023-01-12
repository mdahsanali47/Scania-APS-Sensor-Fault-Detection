import os
import sys
import shutil

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import (ModelPusherArtifact,ModelEvaluationArtifact
                                           )


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact):

        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            # get the trained model file path
            trained_model_file_path = self.model_evaluation_artifact.trained_model_path

            # create model pusher directory to save the model
            model_file_path = self.model_pusher_config.model_pusher_model_file_path
            os.makedirs(model_file_path, exist_ok=True)
            shutil.copy(src = trained_model_file_path, dst = model_file_path)

            # create the saved_model_dir:
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(saved_model_path, exist_ok=True)
            shutil.copy(src = trained_model_file_path, dst = saved_model_path)

            # create the model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(
                model_file_path=model_file_path,
                save_model_path=saved_model_path
            )
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
