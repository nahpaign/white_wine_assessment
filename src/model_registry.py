"""This module handles saving and loading the model and its metadata
"""

from src.config import appconfig
import logging
from joblib import dump, load
import json
import os

logging.basicConfig(level=logging.INFO)

models_dir = appconfig['Directories']['models']
metadata_dir = appconfig['Directories']['metadata']

def get_version(model_name):
    """Determine version number for a given model.
    """
    os.makedirs(metadata_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    versions = [0]
    for file in os.listdir(metadata_dir):
        if file.startswith(model_name):
            version = int(file.split('_v')[-1].split('.')[0])
            versions.append(version)
    return max(versions) + 1



def register(model, model_metadata):
    """Creates models and metadata directories if they don't exist.
    Saves model to pickle.
    Saves metadata dict as JSON.
    """

    # Create directories if not exists
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    # Get version
    version = get_version(model_metadata['name'])
    
    # Save model
    model_filename = f"{model_metadata['name']}_v{version}.pkl"
    model_path = os.path.join(models_dir, model_filename)
    dump(model, model_path)
    model_metadata['model'] = model_filename 

    # Save metadata
    metadata_filename = f"{model_metadata['name']}_v{version}.json"
    model_metadata_path = os.path.join(metadata_dir, metadata_filename)
    with open(model_metadata_path, 'w') as f:
        json.dump(model_metadata, f, indent=4)
    
    logging.info(f"Registered successfully: {model_metadata['name']}")
    return model_metadata_path

def get_metadata(model_name, version=None):
    if version is None:
        version = get_version(model_name) - 1
    metadata_path = os.path.join(metadata_dir, f"{model_name}_v{version}.json")
    if not os.path.exists(metadata_path):
        logging.warning(f"No metadata found for {model_name} v{version}")
        return None
    with open(metadata_path, 'r') as f:
        logging.info(f"Metadata loaded: {model_name} v{version}")
        return json.load(f)


def retrieve(model_name, version=None):
    """Retrieves a model and its metadata by name and version (optional)
    """
    if version is None:
        version = get_version(model_name) - 1
    logging.info(f"Retrieving {model_name} v{version}")
    model_metadata_path = os.path.join(metadata_dir, f"{model_name}_v{version}.json")
    
    # Load metadata
    with open(model_metadata_path, 'r') as f:
        metadata = json.load(f)

    # Load model
    model = load(os.path.join(models_dir, metadata['model']))
    logging.info(f"Retrieved {model_name} v{version} successfully")
    return model, metadata['features'] 