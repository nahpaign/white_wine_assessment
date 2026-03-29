"""This module automates the model training process.
"""

import argparse
import logging

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 

from src import data_processor
from src import model_registry
from src import evaluation
from src.config import appconfig

logging.basicConfig(level=logging.INFO)

features = appconfig['Model']['features'].split(',')
label = appconfig['Model']['label']

def run(data_path):
    """Main script to perform model training.
        Parameters:
        data_path(str): Directory to training set in csv.
        Returns:
            None: No returns required.
    """
    logging.info('Processing data...')
    df = data_processor.run(data_path)

    # Training data has no categorical features.
    # Train-Test split
    logging.info('Train-Test splitting...')
    X_train, X_test, y_train, y_test = train_test_split(df[features],
                                                        df[label],
                                                        test_size=appconfig.getfloat('Model', 'test_size'), \
                                                        random_state=42)
    # Train Classifier
    logging.info('Start model training...')
    lr = LinearRegression()

    lr.fit(X_train, y_train)

    # Evaluate and persist
    if evaluation.run(y_test, lr.predict(X_test)):
        logging.info('Persisting model...')
        mdl_meta = {'name': appconfig['Model']['name'], \
                    'features': features, \
                    'metrics': evaluation.get_eval_metrics(y_test, lr.predict(X_test))}
        model_registry.register(lr, mdl_meta)

        logging.info('Training completed!')
        return None
    

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    args = argparser.parse_args()
    run(args.data_path)