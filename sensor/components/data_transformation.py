import os
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek


from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import DataTransformationConfig, TrainingPipelineConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, DataValidatoinArtifact

from sensor.constant.training_pipeline import TARRGET_COLUMN
from sensor.ml.model.estimator import TargetValueMapping

from sensor.utils.main_utils import save_numpy_array, load_numpy_array, save_python_object


class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidatoinArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transfomer_object(cls) -> Pipeline:
        try:
            robust_scaler = RobustScaler()
            imputer = SimpleImputer(strategy='mean')

            preprocessing_pipeline = Pipeline([
                ('robust_scaler', robust_scaler),
                ('imputer', imputer)
            ])

            return preprocessing_pipeline

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:

            # read data for transformation from data validation artifact
            train_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path)

            # get data transformer object
            preprocessing_pipeline = DataTransformation.get_data_transfomer_object()

            # get input depenedent (y) and independent(X) features from train_df
            input_features_train_df = train_df.drop(
                columns=[TARRGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARRGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(
                TargetValueMapping().to_dict())

            # get input depenedent (y) and independent(X) features from train_df
            input_features_test_df = test_df.drop(
                columns=[TARRGET_COLUMN], axis=1)
            target_features_test_df = test_df[TARRGET_COLUMN]
            target_features_test_df = target_features_test_df.replace(
                TargetValueMapping().to_dict())

            # fit and transform train and test data
            preprocessing_object = preprocessing_pipeline.fit(
                input_features_train_df)

            transformed_input_features_train_df = preprocessing_object.transform(
                input_features_train_df)

            transformed_input_features_test_df = preprocessing_object.transform(
                input_features_test_df)

            # balance train and test data
            smt = SMOTETomek(random_state=42, sampling_strategy="not majority")

            input_features_train_rs, target_feature_train_rs = smt.fit_resample(
                transformed_input_features_train_df, target_feature_train_df)

            input_features_test_rs, target_feature_test_rs = smt.fit_resample(
                transformed_input_features_test_df, target_features_test_df)

            # concatenate dependent and independent features
            train_array = np.c_[
                input_features_train_rs, np.array(target_feature_train_rs)]

            test_array = np.c_[
                input_features_test_rs, np.array(target_feature_test_rs)]

            # save train.npy and test.npy data
            save_numpy_array(
                numpy_array=train_array, file_path=self.data_transformation_config.data_transformation_train_file_path)

            save_numpy_array(
                numpy_array=test_array, file_path=self.data_transformation_config.data_transformation_test_file_path)

            # save preprocessing object
            save_python_object(
                python_object=preprocessing_object, file_path=self.data_transformation_config.data_transformation_transformed_object_file_path)

            # create data transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=os.path.join(
                    self.data_transformation_config.data_transformation_train_file_path),
                transformed_test_file_path=os.path.join(
                    self.data_transformation_config.data_transformation_test_file_path),
                transformed_object_file_path=os.path.join(
                    self.data_transformation_config.data_transformation_transformed_object_file_path))

            logging.info(
                f" Data transformation artifact created {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)
