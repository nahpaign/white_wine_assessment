import configparser
from pathlib import Path

appconfig = configparser.ConfigParser()
appconfig.read(Path(__file__).parent.parent / 'config.ini')