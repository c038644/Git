##########################################################
import json
import pandas as pd
import numpy as np
import pickle
import warnings
import uvicorn
from fastapi import FastAPI

warnings.filterwarnings("ignore")

#app = Flask(__name__)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

@app.post('/local/')

def local():

  #Local Features Case for a chosen Selected Customer
  test_df = pd.read_csv("files/P7_test_df.csv")

  Selected_Customer = pd.read_csv("files/selection.csv")

  print('files loaded')

  Selected_Customer = Selected_Customer.drop(columns=['Unnamed: 0'])
  test_df = test_df.drop(columns=['Unnamed: 0'])

  print(Selected_Customer.shape)
  print(test_df.shape)

  feature_list = list(test_df.columns)

  X = test_df.drop(['TARGET'], axis=1).values
  y = test_df['TARGET'].values

  data = Selected_Customer.drop(['TARGET'], axis=1).values

  filename = 'files/final_model.sav'
  loaded_model = pickle.load(open(filename, 'rb'))
  #result = loaded_model.score(X, y)
  
  print('RFC')

  score = loaded_model.fit(X, y).predict(data)

  Credit_given_test = np.max(loaded_model.predict_proba(data))

  if score==0:
    credit_score=Credit_given_test

  else:
    credit_score=(1-Credit_given_test)

  print('Get importances')

  # Get numerical feature importances
  importances = list(loaded_model.feature_importances_)

  # List of tuples with variable and importance
  feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

  # Sort the feature importances by most important first
  feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

  #Ten most important features
  ten_most_important = feature_importances[0:10]

  ten_most_important_df = pd.DataFrame(ten_most_important)

  ten_most_important_df.columns = ['Feature', 'Importance']

  ten_most_important_df['Credit Score'] = credit_score

  ten_most_important_df['Credit Granted?'] = None

  if credit_score>=0.35:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Yes')
  elif credit_score>=0.25:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('Risky')
  else:
    ten_most_important_df['Credit Granted?'] = ten_most_important_df['Credit Granted?'].fillna('No')

  ten_most_important_df.to_csv("files/Customer_score.csv")

  print('Customer Score Ready')
  return json.dumps(ten_most_important_df.to_json())


@app.route('/global_data/')

def global_data():

  test_df = pd.read_csv("files/P7_test_df.csv")
  test_df = test_df.drop(columns=['Unnamed: 0'])

  print('files loaded')

  #Global Features Case

  feature_list = list(test_df.columns)

  X = test_df.drop(['TARGET'], axis=1).values
  y = test_df['TARGET'].values

  print('RFC')
  
  filename = 'files/final_model.sav'
  loaded_model = pickle.load(open(filename, 'rb'))
  
  print('Get importances')

  # Get numerical feature importances
  importances = list(loaded_model.feature_importances_)

  # List of tuples with variable and importance
  feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

  # Sort the feature importances by most important first
  feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

  #Ten most important features
  ten_most_important = feature_importances[0:10]

  Global_Features = pd.DataFrame(ten_most_important)

  Global_Features.columns = ['Feature', 'Importance']

  print('Global Features Ready')

  Global_Features.to_csv("files/Global_Features.csv")

  # Print out the feature and importances 
  return json.dumps(Global_Features.to_json())

#if __name__ == "__main__":
#    app.run(debug=True)
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
