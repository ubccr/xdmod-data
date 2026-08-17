# Read the minimum supported Python version from setup.cfg
import configparser
from pathlib import Path
project_dir = Path(__file__).resolve().parents[3]
config = configparser.ConfigParser()
config.read(project_dir / 'setup.cfg')
print(config['options']['python_requires'].removeprefix('>='))
