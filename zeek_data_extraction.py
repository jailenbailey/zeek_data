"""
Import Libraries
"""
# Data/environment imports
import os
import glob
import pandas as pd
import concurrent.futures
from zat.json_log_to_dataframe import JSONLogToDataFrame
"""
Initialize JSONLogToDataFrame and create a path variable
"""
# ZAT is awesome for creating this LogToDataFrame functionality
log_to_df = JSONLogToDataFrame()
# Get the entire dir
files_path = ''
"""
The following 4 functions to go through every file in the specified month and grab the conn logs
"""
# Function to get the days from the 1st to the 9th of the month
def one_third_month(files_path):
  # Get everything under the dir
  read_files = glob.glob(os.path.join(files_path, ''))
  # Get the first file to fit the parameters
  df = log_to_df.create_dataframe(read_files[0])
  # Nice little loop that is going to take forever
  for files in range(1, len(read_files)):
    # Create a new DataFrame to read files from within the given range/parameters
    temp_df = log_to_df.create_dataframe(read_files[files])
    # Join the 2 dataframes
    df = pd.concat([df, temp_df])
    # print len to make sure everything goes smoothly
    print(files)
  # Reset Index
  df = df.reset_index()
  # Return the df
  return df
# Function to get the days from 11th to 19th of the month
def two_thirds_month(files_path):
  # Get everything under the dir
  read_files = glob.glob(os.path.join(files_path, ''))
  # Get the first file to fit the parameters
  df = log_to_df.create_dataframe(read_files[0])
  # Nice little loop that is going to take forever
  for files in range(1, len(read_files)):
    # Create a new DataFrame to read files from within the given range/parameters
    temp_df = log_to_df.create_dataframe(read_files[files])
    # Join the 2 dataframes
    df = pd.concat([df, temp_df])
    # print len to make sure everything goes smoothly
    print(files)
  # Reset Index
  df = df.reset_index()
  # Return the df
  return df
# Function to get the days from 20th to 29th of the month
def three_thirds_month(files_path):
  # Get everything under the dir
  read_files = glob.glob(os.path.join(files_path, ''))
  # Get the first file to fit the parameters
  df = log_to_df.create_dataframe(read_files[0])
  # Nice little loop that is going to take forever
  for files in range(1, len(read_files)):
    # Create a new DataFrame to read files from within the given range/parameters
    temp_df = log_to_df.create_dataframe(read_files[files])
    # Join the 2 dataframes
    df = pd.concat([df, temp_df])
    # print len to make sure everything goes smoothly
    print(files)
  df = df.reset_index()
  return df
# Function to get the 30 days if they exist, might create a conditional if they exist or not, but this works for now
def thirtieth_days(files_path):
  # Get everything under the dir
  read_files = glob.glob(os.path.join(files_path, ''))
  # Get the first file to fit the parameters
  df = log_to_df.create_dataframe(read_files[0])
  # Nice little loop that is going to take forever
  for files in range(1, len(read_files)):
    # Create a new DataFrame to read files from within the given range/parameters
    temp_df = log_to_df.create_dataframe(read_files[files])
    # Join the 2 dataframes
    df = pd.concat([df, temp_df])
    # print len to make sure everything goes smoothly
    print(files)
  # Reset Index
  df = df.reset_index()
  # Return the df
  return df  
"""
Main function to run each function above and concat the results
"""
# Main function
def main():
  # Initializing the executor
  with concurrent.futures.ProcessPoolExecutor() as executor:
    # One executor for each function
    f1 = executor.submit(one_third_month, files_path)
    f2 = executor.submit(two_thirds_month, files_path)
    f3 = executor.submit(three_thirds_month, files_path)
    f4 = executor.submit(thirtieth_days, files_path)
    # Combine the results into a list
    frames = [f1.result(), f2.result(), f3.result(), f4.result()]
    # Concat all results (separate frames) to one frame
    df = pd.concat(frames)
    # Out to csv with all data
    df.to_csv('')
"""
Execute the main function
"""
# If name == main, start the main function
if __name__ == '__main__':
    main()