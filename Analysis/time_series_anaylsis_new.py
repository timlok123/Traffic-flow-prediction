
# Import module 
import tensorflow as tf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
#MeanSquaredError - find the difference between valid and train 
from tensorflow.keras.losses import MeanSquaredError  
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam

# Use a function to group all the thingss
def analysis_function(csv_path, window_size=100,epoch_no=50,learning_rate = 0.001,time_interval = "30min",location=None):
  directory_path = os.getcwd()

  df = pd.read_csv(csv_path,dtype ={'Datetime':str,'Count':np.int64})

  ### 1. Reformat the 1st col ---------------------------------------------------------------------------------------------###
  df["Datetime"]= df["Datetime"].str.replace("_","-",2)
  df["Datetime"]= df["Datetime"].str.replace("_"," ",1)
  df["Datetime"]= df["Datetime"].str.replace("_",":",2)


  ### 2. Resample the data in the 30 mins ----------------------------------------------------------------------------------###
  # "H" groups the data in the same hour
  # "10min" groups the data in the same 10 mins
  # Set the index column to be datetime
  df.Datetime = pd.to_datetime(df.Datetime)
  df.index = df["Datetime"]
  df = df.groupby(pd.Grouper(key='Datetime', freq=time_interval)).sum()

  ### 3. Build the model and do analysis ----------------------------------------------------------------------------------###
  # Create the matrix we need for analysis
  # The structure of X and Y are like
  # If window_size = 5 
  # 0th X = [[[1st Count],[2nd Count],[3rd Count],[4th Count],[5th Count]]] 
  # 0th Y = [6th Count]
  # 1st X = [[[2nd Count],[3rd Count],[4th Count],[5th Count],[6th Count]]] 
  # 1st Y = [7th Count]
  # ... 

  # window_size - how many input you use to intrepret 1 output
  def df_to_X_y(df, window_size=5):
    df_as_np = df.to_numpy()
    X = []
    Y = []

    for i in range(len(df_as_np)-window_size):
      row = [a for a in df_as_np[i:i+window_size]]
      X.append(row)
      Y.append(df_as_np[i+window_size][0])
    return np.array(X), np.array(Y)

  X,Y = df_to_X_y(df, window_size)

  # train_percentage = How many % of X are used to train the model 
  # valid_percentage = How many % of X are used to validate

  train_percentage = 0.8
  valid_percentage = 0.1

  train_range = int(len(X)*train_percentage)
  val_range = int(len(X)*valid_percentage)

  x_train, y_train = X[:train_range], Y[:train_range]
  x_valid, y_valid = X[train_range:train_range+val_range], Y[train_range:train_range+val_range]
  x_test, y_test = X[train_range+val_range:], Y[train_range+val_range:]

  x_train.shape, y_train.shape, x_valid.shape, y_valid.shape, x_test.shape, y_test.shape

  model = Sequential()
  # numbers of window_size input, 1 input
  model.add(InputLayer((window_size, 1)))
  model.add(LSTM(64))
  model.add(Dense(8, "relu"))
  model.add(Dense(1, "linear"))

  # save_best_only = The one only has smallest lost 
  ## need to change the path on local computer
  cp1 = ModelCheckpoint(directory_path, save_best_only=True)
  model.compile(loss=MeanSquaredError(), 
                optimizer=Adam(learning_rate=learning_rate), 
                metrics=[RootMeanSquaredError()])

  #epochs - how many times you iterate
  model.fit(x_train,
            y_train, 
            validation_data=(x_valid, y_valid),
            epochs=epoch_no,
            callbacks=[cp1])
  model.save('my_model.h5')

  ### 4. Load the model and visualize the result -------------------------------------------------------------------------###
  from tensorflow.keras.models import load_model

  model_path = os.path.join(directory_path,"my_model.h5")

  model = load_model(model_path)

  train_predictions = model.predict(x_train).flatten()
  train_results = pd.DataFrame(data={'Train Predictions':train_predictions, 'Actuals':y_train})
  train_results

  """
  import matplotlib.pyplot as plt
  print(train_results["Train Predictions"])
  print(train_results["Actuals"])
  plt.plot(train_results["Train Predictions"])
  plt.plot(train_results["Actuals"]
  """

  #plot the val and predicted curve 
  val_predictions = model.predict(x_valid).flatten()
  val_results = pd.DataFrame(data={'Val Predictions':val_predictions, 'Actuals':y_valid})
  plt.plot(val_results['Val Predictions'],label="Predictions",color="blue")
  plt.plot(val_results['Actuals'],label="Actual result(validate)",color="red")
  plt.title("Validation & Acutal result plot of " + str(location))
  plt.legend()
  plt.show()

  #plot the test and predicted curve 
  test_predictions = model.predict(x_test).flatten()
  test_results = pd.DataFrame(data={'Test Predictions':test_predictions, 'Actuals':y_test})
  plt.plot(test_results['Test Predictions'],label="Predictions",color="blue")
  plt.plot(test_results['Actuals'],label="Actual result(Test)",color="red")
  plt.title("Test & Acutal result plot of " + str(location))
  plt.legend()
  plt.show()

#path - window_size=100,epoch_no=30,learning_rate = 0.001
csv_path = os.path.join(os.getcwd(),"[AID01111].csv")

#path1 - window_size=100,epoch_no=30,learning_rate = 0.001
csv_path1 = os.path.join(os.getcwd(),"[AID01213].csv")

csv_location_dict = {"[AID01111]":csv_path,"[AID01213]":csv_path1}

for i in csv_location_dict:
  analysis_function(csv_location_dict[i], 
                      window_size=100,
                          epoch_no=30,
                    learning_rate = 0.001,
                    time_interval = "30min", 
                   location=i)

"""
#path2 - window_size=50,epoch_no=30,learning_rate = 0.001
csv_path2 = os.path.join(os.getcwd(),"[AID03106].csv") 

#path3 - window_size=5,epoch_no=30,learning_rate = 0.001
#This position has too few cars, hard to have meaningful result 
#Better use a smaller window to analyze this 
csv_path3 = os.path.join(os.getcwd(),"[AID03211].csv")

#path4 - window_size=100,epoch_no=30,learning_rate = ,0.001
csv_path4 = os.path.join(os.getcwd(),"[TDSIEC10001].csv")
csv_path_list = [csv_path,csv_path1,csv_path2,csv_path3,csv_path4]
location = ["[AID01111]","[AID01213]","[AID03106]","[AID03211]","[TDSIEC10001]"]
"""
