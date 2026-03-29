from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from src.model_registry import retrieve
from src.config import appconfig

app = FastAPI()

model, features = retrieve(appconfig['Model']['name'])

@app.get(appconfig['API']['home'])
def home():
    return {"message": "Welcome to DSSI Day 3 Workshop 1!"}

@app.post(appconfig['API']['white_wine_quality'])
def predict(data: dict):
    """Endpoint to retrieve predicted quality given input data from request.
        Params:
            data dict: input from request
        Returns:
            JSON: "Quality" as key and predicted value.
     """
    pred_df = pd.DataFrame.from_dict([data])
    pred = model.predict(pred_df[features])
    return {'Quality': float(pred[0])}