"""Imports"""
# Data manipulation/analysis libraries
import numpy as np
import pandas as pd
# Models/performance/metrics
import xgboost as xgb
from sklearn.model_selection import train_test_split

"""Cleaning/grouping/resampling function to create generically useable data"""
def groupby_time(base_df):
  # Initialize the ts column as a type datetime
  base_df['ts'] = pd.to_datetime(base_df['ts'])
  # Parse the time to remove all unwanted values
  base_df['ts'] = base_df['ts'].dt.strftime('%Y-%m-%d %H:%M')
  # Create a new frame to group the unique values by size
  df = base_df.groupby(['ts']).size()
  # Reassign the new frame to create the new column
  df = base_df.join(df.to_frame(), on='ts')
  # Drop all duplicate entries, leaving only the unique entries
  df = df.drop_duplicates(subset=['ts'])
  # New df to not have to list all columns to drop
  zeek_df = df[['ts', 0]]
  # Rename the column
  zeek_df = zeek_df.rename(columns={0 : 'log_counts'})
  # Set the index to the ts column
  zeek_df = zeek_df.set_index('ts')
  # Set index to a type of datetime
  zeek_df.index = pd.to_datetime(zeek_df.index)
  # Return newly formatted df
  return zeek_df
"""Function to create specific features for the model"""
def create_features(df):
  # Make month column
  df['month'] = df.index.month
  # Make day column
  df['day'] = df.index.day
  # Make hour column
  df['hour'] = df.index.hour
  # Make minute column
  df['minute'] = df.index.minute
  # Make day of year column
  df['day_of_year'] = df.index.day_of_year
  # Return df
  return df
"""Creating Lag Features as another option to feed information to the model"""
def add_lags(df):
  # Call the create features function
  df = create_features(df)
  # Create a target map
  target_map = df['log_counts'].to_dict()
  # Create lag feature for 1 day in the past
  df['lag1'] = (df.index - pd.Timedelta('1 day')).map(target_map)
  # Create lag feature for 7 days in the past
  df['lag7'] = (df.index - pd.Timedelta('7 days')).map(target_map)
  # Create lag feature for 14 days in the past
  df['lag14'] = (df.index - pd.Timedelta('14 days')).map(target_map)
  # Return finished function
  return df
"""Function to divide the data by features and percentage, and then train/fit the model"""
def split_train_test_model(df):
  # Call the add_lags function
  df = add_lags(df)
  # Rearrange the columns
  df = df[['month', 'day', 'day_of_year', 'hour', 'minute', 'lag1', 'lag7', 'lag14' 'log_counts']]
  # X Value to get everything but the last column in the DF
  X = df.iloc[:, :-1]
  # y value to get only the last column in the DF
  y = df.iloc[:, -1]
  # Using SKlearns train_test_split
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)
  # Create model
  reg = xgb.XGBRegressor(base_score=0.5,
                       booster='gbtree',    
                       n_estimators=100,
                       objective='reg:squarederror',
                       max_depth=3,
                       learning_rate=0.01,
                       colsample_bytree=0.3,
                       colsample_bylevel=0.4,
                       subsample=0.89)
  # Fit the model 
  reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=100)
  # Return the trained model
  return reg
"""Get the path to the data and run the functions"""
def main():
  # Firsly, get user input for the path to the data
  data_path = input('Path to your data (CSV for now): ')
  # Read the data into csv format
  df = pd.read_csv(data_path)
  # Call the model function, which will run the whole program
  model = split_train_test_model(df)
  # Model to JSON for now
  model.save_model('xbg_reg_zeek_model_minute.json')
  # No need to return anything, the model in a file is all we want
  return
# If name == main, start the main function
if __name__ == '__main__':
    main()
