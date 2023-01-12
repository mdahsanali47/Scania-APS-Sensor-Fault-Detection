
import os
import sys

from sensor.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from sensor.exception import SensorException


class TargetValueMapping:
    """
        Mapping target variable values to numeric values 0 and 1
    """

    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, X):
        try:
            X_transformed = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transformed)
            return y_hat
        except Exception as e:
            raise SensorException(e, sys)


class ModelResolver:
    """
        To get the best model if exists
    """

    def __init__(self, models_dir=SAVED_MODEL_DIR):
        try:
            self.models_dir = models_dir
        except Exception as e:
            raise SensorException(e, sys)

    def get_best_model_path(self):
        """
            Get the best model path
        """
        try:
            timestamp = map(int, os.listdir(self.models_dir))
            latest_timestamp = max(timestamp)
            latest_model_path = os.path.join(
                self.models_dir, str(latest_timestamp), MODEL_FILE_NAME)
            return latest_model_path

        except Exception as e:
            raise SensorException(e, sys)

    def is_model_exists(self) -> bool:
        """
            Check if model exists
        """
        try:

            if not os.path.exists(self.models_dir):
                return False
            timestamp = os.listdir(self.models_dir)
            if len(timestamp) == 0:
                return False
            latest_model_path = self.get_best_model_path()
            if not os.path.exists(latest_model_path):
                return False
            return True

        except Exception as e:
            raise SensorException(e, sys)
            
