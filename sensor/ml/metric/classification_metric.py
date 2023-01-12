from sensor.exception import SensorException
from sensor.logger import logging

import os
import sys
from sklearn.metrics import f1_score, recall_score, precision_score

from sensor.entity.artifact_entity import ClassificationMetricsArtifact


def get_classification_score(y_true, y_pred) -> ClassificationMetricsArtifact:
    try:

        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metrics = ClassificationMetricsArtifact(
            f1_score=model_f1_score,
            recall_score=model_recall_score,
            precision_score=model_precision_score
        )
        logging.info(f"classification metrics calculated successfully {classification_metrics}")
        return classification_metrics

    except Exception as e:
        raise SensorException(e, sys)
