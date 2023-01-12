

from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_pathe: str


@dataclass
class DataValidatoinArtifact:
    validaton_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

# artifact for model trainer


@dataclass
class ClassificationMetricsArtifact:
    f1_score: float
    precision_score: float
    recall_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricsArtifact
    test_metric_artifact: ClassificationMetricsArtifact


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    trained_model_metrics_artifact: ClassificationMetricsArtifact
    best_model_metrics_artifact: ClassificationMetricsArtifact

@dataclass
class ModelPusherArtifact:
    save_model_path:str
    model_file_path:str