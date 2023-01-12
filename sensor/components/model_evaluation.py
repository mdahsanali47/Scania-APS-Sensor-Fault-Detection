import os
import sys
import pandas as pd

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import TrainingPipelineConfig, ModelEvaluationConfig
from sensor.entity.artifact_entity import ModelEvaluationArtifact, ClassificationMetricsArtifact, DataValidatoinArtifact, ModelTrainerArtifact

from sensor.constant.training_pipeline import TARRGET_COLUMN, MODEL_FILE_NAME
from sensor.ml.model.estimator import TargetValueMapping, ModelResolver
from sensor.utils.main_utils import load_python_object, write_yaml_file
from sensor.ml.metric.classification_metric import get_classification_score


class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_validation_artifact: DataValidatoinArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self):
        try:
            # getting file path of valid train and test data.csv
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            # concatenate valid train and test data.csv
            valid_train_df = pd.read_csv(valid_train_file_path)
            valid_test_df = pd.read_csv(valid_test_file_path)
            df = pd.concat([valid_train_df, valid_test_df], axis=0)
            # get the input and target dataframe
            y_true = df[TARRGET_COLUMN]
            y_true = y_true.map(TargetValueMapping().to_dict())
            df = df.drop(columns=[TARRGET_COLUMN], axis=1)

            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()

            is_model_eccepted = True
            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_eccepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    best_model_metrics_artifact=None,
                    trained_model_path=trained_model_file_path,
                    trained_model_metrics_artifact=self.model_trainer_artifact.test_metric_artifact
                )
                logging.info("model_evaluation_artifact : {}".format(
                    model_evaluation_artifact))
                write_yaml_file(data = model_evaluation_report,
                            yaml_file_path = self.model_evaluation_config.model_evaluation_report_file_path, replace=True)
                return model_evaluation_artifact

            # get the model

            latest_model_file_path = os.path.join(
                model_resolver.get_best_model_path(), MODEL_FILE_NAME)
            latest_model = load_python_object(latest_model_file_path)
            trained_model = load_python_object(trained_model_file_path)

            # prediction using the models to compare
            # 1. trained model
            y_trained_pred = trained_model.predict(df)
            # 2. latest model
            y_latest_pred = latest_model.predict(df)

            # trained and latest model metrics
            train_metrics = get_classification_score(y_true, y_trained_pred)
            latest_metricss = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = train_metrics.f1_score - latest_metricss.f1_score
            if improved_accuracy > self.model_evaluation_config.model_evaluation_improved_score:
                is_model_eccepted = True
            else:
                is_model_eccepted = False
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_eccepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_file_path,
                trained_model_path=trained_model_file_path,
                trained_model_metrics_artifact=train_metrics,
                best_model_metrics_artifact=latest_metricss
            )

            model_evaluation_report = model_evaluation_artifact.__dict__

            # saving model evaluation report
            write_yaml_file(data = model_evaluation_report,
                            yaml_file_path = self.model_evaluation_config.model_evaluation_report_file_path, replace=True)

            logging.info("model_evaluation_artifact : {}".format(
                model_evaluation_artifact))
            return model_evaluation_artifact

        except Exception as e:
            raise SensorException(e, sys)
