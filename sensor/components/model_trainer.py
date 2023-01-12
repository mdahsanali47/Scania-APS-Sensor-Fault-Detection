import os
import sys

from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import ModelTrainerConfig, TrainingPipelineConfig
from sensor.entity.artifact_entity import ClassificationMetricsArtifact, ModelTrainerArtifact, DataTransformationArtifact
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import load_numpy_array, load_python_object, save_python_object


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:

        try:

            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self, X_train, y_train):
        try:
            # best model for this problem statement is XGBoostClassifier, notebook attached
            xgb_clf = XGBClassifier()
            xgb_clf.fit(X_train, y_train)
            return xgb_clf

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self):
        try:

            # load numpy array
            transformed_train_df = load_numpy_array(
                self.data_transformation_artifact.transformed_train_file_path)
            transformed_test_df = load_numpy_array(
                self.data_transformation_artifact.transformed_test_file_path)

            # split train and test array to X and y
            X_train = transformed_train_df[:, :-1]
            y_train = transformed_train_df[:, -1]
            X_test = transformed_test_df[:, :-1]
            y_test = transformed_test_df[:, -1]

            # train model
            model = self.train_model(X_train, y_train)
            y_train_pred = model.predict(X_train)
            classification_train_metrics = get_classification_score(
                y_train, y_train_pred)

            # check if model pass the threshold score/accuracy
            if classification_train_metrics.f1_score < self.model_trainer_config.model_training_threshold_score:
                raise SensorException(
                    "trained model failed , accuracy is lower than expected.")

            y_test_pred = model.predict(X_test)
            classification_test_metrics = get_classification_score(
                y_test, y_test_pred)

            # check for over fitting and under fitting
            if abs(classification_train_metrics.f1_score - classification_test_metrics.f1_score) > self.model_trainer_config.model_training_under_over_fitting_threshold:
                raise SensorException(
                    "Model training failed , model is over fitting or under fitting.")

            # load preprocessor
            preprocessor = load_python_object(
                self.data_transformation_artifact.transformed_object_file_path)

            # save model
            """model_dir_path = os.path.join(
                self.model_trainer_config.model_training_trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)"""
            sensor_model = SensorModel(preprocessor=preprocessor, model=model)

            save_python_object(python_object=sensor_model,
                               file_path=self.model_trainer_config.model_training_trained_model_file_path)

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                train_metric_artifact=classification_train_metrics,
                test_metric_artifact=classification_test_metrics,
                trained_model_file_path=self.model_trainer_config.model_training_trained_model_file_path
            )
            logging.info(
                f"Model training completed successfully.")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
