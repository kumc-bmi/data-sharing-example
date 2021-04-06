# import libraries and dependencies needed
from opencage.geocoder import OpenCageGeocode
from datetime import timedelta, datetime
from statsmodels.formula.api import ols
from IPython.display import HTML
from dotenv import load_dotenv
from random import randint
from random import choice as rc
from pprint import pprint
from scipy import stats
import matplotlib.pyplot as matplot
import seaborn
import itertools
import statsmodels.api as sma
import numpy as np
import pandas as pd
import sqlite3
import math
import warnings
import os

# filter unwanted warning
warnings.filterwarnings('ignore')

# load dotenv to read env variable
load_dotenv()

# assign opencage API key to variabl opencage_api_key 
opencage_api_key = os.environ.get("opencage_api_key")

# Declear database
DATABASE = "db/Northwind_large.sqlite"

# database connection
connection = sqlite3.connect(DATABASE)
db_connection = connection.cursor()

# Northwind Tables
north_tables = db_connection.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
north_tables = [i[0] for i in north_tables]

# Convert tables to dataframes
data_frames = []
for i in north_tables:
  table = db_connection.execute('SELECT * FROM "'+i+'"').fetchall()
  columns = db_connection.execute('PRAGMA table_info("'+i+'")').fetchall()
  panda_data_frame = pd.DataFrame(table, columns=[i[1] for i in columns])
  table_name = i
  exec(table_name + " = panda_data_frame")
  data_frames.append(table_name)

# Set panda to display float values to four decimal places
pd.options.display.float_format = "{:,.4f}".format