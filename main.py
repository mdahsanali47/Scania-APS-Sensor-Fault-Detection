import os
import sys
import pandas as pd

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.utils.main_utils import load_python_object
from sensor.constant.application import APP_HOST, APP_PORT

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from starlette.responses import RedirectResponse

app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:

        training_pipeline = TrainingPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training Pipeline is already running")

        training_pipeline.run_pipeline()
        return Response("Training Successfull !!")

    except Exception as e:
        return Response(f"Error Occured: {e}")


@app.get("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:

        # get csv file from user and convet to dataframe
        df = pd.read_csv(file.file)
        model_resolver = ModelResolver(models_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        # predict the data
        best_model_path = model_resolver.get_best_model_path()
        model = load_python_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_columns'] = y_pred
        df["predicted_columns"].replace(
            TargetValueMapping().reverse_mapping(), inplace=True)
        return df.to_html()

    except Exception as e:
        return Response(f"Error Occured: {e}")

if __name__ == '__main__':
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
