import sys
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainingPipeline


def test_exception():
    try:
        # logging.info("test_exception as we are dividing it by zero")

        x = 1/0
    except Exception as e:
        raise SensorException(e, sys)


if __name__ == '__main__':
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        raise SensorException(e, sys)
