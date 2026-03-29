"""This module evaluates the model performance.
"""

import logging
from sklearn.metrics import r2_score, mean_squared_error
from src.config import appconfig

logging.basicConfig(level=logging.INFO)

# loads the threshold
r2_min = appconfig.getfloat('Evaluation', 'r2')
# load model and model name

def get_eval_metrics(y_true, y_pred):
    """
    Returns model evaluation metrics.
        Params:
            y_true: True labels
            y_pred: Predicted labels
        Returns:
        dict: Dictionary containing evaluation metrics
        """
    results = {'r2': round(r2_score(y_true, y_pred), 2),
               'mse': round(mean_squared_error(y_true, y_pred), 2)}
    return results

def run(y_true, y_pred):
    """
    Evalues model performance based on R2 against a minimum threshold.
        Params:
            y_true: True labels
            y_pred: Predicted labels
        Returns:
            bool: True if evaluation passes, False if fails.
            """
    logging.info('Evaluating model...')
    metrics = get_eval_metrics(y_true, y_pred)
    logging.info(f"R2: {metrics['r2']}, MSE: {metrics['mse']}")
    new_r2 = metrics['r2']
    

    if new_r2 < r2_min:
        logging.warning(f"Model evaluation failed: R2 {new_r2} < threshold {r2_min}")
        return False
    
    logging.info('Model Evaluation Passed...')
    return True
