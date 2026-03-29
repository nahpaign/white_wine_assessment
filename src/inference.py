"""This module contains model inference.
"""

import pandas as pd
from src import model_registry
from src.config import appconfig

clf, features = model_registry.retrieve(appconfig['Model']['name'])

def get_prediction(**kwargs):
    """
    Gets prediction for a given data set.
        Params:
        kwargs: Keyword argument list containing data for prediction.
        Returns:
            Predicted class in float.
    """
    pred_df = pd.DataFrame(kwargs, index=[0])
    pred = clf.predict(pred_df[features])
    return float(pred[0])