import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import requests
import json
import csv
import numpy as np
import pandas as pd

activity_df = pd.read_csv('data/preprocess/activity.csv')

print(activity_df['content'])
