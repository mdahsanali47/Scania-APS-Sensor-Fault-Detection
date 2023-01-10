

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp
import numpy as np

from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.config_entity import DataValidationConfig, TrainingPipelineConfig, DataIngestionConfig
from sensor.entity.artifact_entity import DataValidatoinArtifact, DataIngestionArtifact

from sensor.constant.training_pipeline import SCHEMA_FILE_PATH, SCHEMA_DROP_COLUMN

from sensor.utils.main_utils import read_yaml_file, write_yaml_file


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_aritfact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_aritfact = data_ingestion_aritfact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Read data from file data ingestion--> ingested--> train and test file path
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise SensorException(e, sys)

    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        """
        Validate number of columns in the data
        """
        try:
            num_of_columns = len(self._schema_config["columns"])
            if num_of_columns == len(df.columns):
                return True
            return False
        except Exception as e:
            raise SensorException(e, sys)

    def is_numerical_columns_exists(self, df: pd.DataFrame) -> bool:
        """
        Check if numerical columns exists in the data
        """
        try:
            numerical_cols = self._schema_config['numerical_columns']
            df_numerical_cols = df.columns

            missing_num_cols = []
            numerical_cols_present = True
            for col in numerical_cols:
                if col not in df_numerical_cols:
                    missing_num_cols.append(col)
                    numerical_cols_present = False
        except Exception as e:
            raise SensorException(e, sys)

    def detect_data_drift(self, base_sample, current_sample, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for col in base_sample.columns:
                d1 = base_sample[col]
                d2 = current_sample[col]

                is_same_dist = ks_2samp(d1, d2)
                if is_same_dist.pvalue > threshold:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {col: {"data_drift_found": is_found, "pvalue": float(is_same_dist.pvalue)}})

            drift_report_file_path = os.path.join(
                self.data_validation_config.drift_report_file_path)
            # creating dir for report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            # writing report file to yaml
            write_yaml_file(yaml_file_path= drift_report_file_path, data= report)
            return status
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self) -> DataValidatoinArtifact:
        """
        Initiate data validation
        """
        try:
            error_message = ""
            train_file_path = self.data_ingestion_aritfact.train_file_path
            test_file_path = self.data_ingestion_aritfact.test_file_pathe

            # read data from train and test file location
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # validate number of columns
            status = self.validate_number_of_columns(train_df)
            if status == False:
                error_message += "Number of columns in train data is not matching with schema file \n"

            status = self.validate_number_of_columns(test_df)
            if status == False:
                error_message += "Number of columns in test data is not matching with schema file \n"

            # validate numerical columns
            status = self.is_numerical_columns_exists(train_df)
            if status == False:
                error_message += "some Numerical columns are missing in train data \n"
            status = self.is_numerical_columns_exists(test_df)
            if status == False:
                error_message += "some Numerical columns are missing in test data \n"

            if len(error_message) > 0:
                raise Exception(error_message)

            # checking data drift
            status = self.detect_data_drift(train_df, test_df)

            # creating data validation artifact
            data_validation_artifact = DataValidatoinArtifact(
                validaton_status=status, valid_train_file_path=self.data_ingestion_aritfact.train_file_path,
                valid_test_file_path=self.data_ingestion_aritfact.test_file_pathe,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path)

            logging.info(f"Data validation artifact created : {data_validation_artifact}")
            return data_validation_artifact


        except Exception as e:
            raise SensorException(e, sys)
