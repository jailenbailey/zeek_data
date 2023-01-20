# Data related libraries
import re
import numpy as np
import pandas as pd
# Zeek Specific 
import zat
from zat.json_log_to_dataframe import JSONLogToDataFrame

# Function to parse the languages by getting the 2nd location in the list
def parse_language(language_string):
  # Getting rid of the brackets
  language_string = banish_brackets(language_string)
  # Using REGEX to find the string with a bracket, which seems exclusive to languages
  re_check = re.findall(r"\[(\w+)\]", language_string)
  # If the length of the element is 0
  if len(re_check) == 0:
    # Return missing
    return 'Missing'
    # If the length of the element is 1
  elif len(re_check) == 1:
    # Get the first location of the list, which is what I want. And using Upper, because abbreviated undercase feels underwhelming
    return re_check[0].upper()
  # Empty function return for my sanity 
  return  
# Logic to strip non digits from browser version
def remove_letters(num_string):
  # Basic for loop, you know the drill
  for i in num_string:
    # This currently works, a little too good actually.
    num_string = re.findall("\d+\.\d+", i)
    # Return what we processed
  return num_string
# Simple logic to get rid of the brackets in each column
def banish_brackets(data):
  # Replace the first position of the empty string with nothing
  data = data[0].replace('\'', '')
  # Return the data
  return data
# Main function to parse the UA String
def main(http_frame):
  # Drop duplicates from the UA String to get all of the unique values
  http_frame = http_frame.drop_duplicates(subset=['user_agent'])
  # Drop na's so we don't result in wonky results
  http_frame = http_frame.dropna(subset=['user_agent'])
  # Empty list
  brow_list = []
  # Empty list
  browser_ver = []
  # Empty list
  user_language = []
  # Empty list
  oper_sys_infras = []
  # The core logice for extracting the data from the string
  for i in http_frame['user_agent']:
    # Thank god this regex pattern works
    parsed_ua = re.findall(r'.+?[/\s]', i)
    # REGEX pattern to get anything with a parenthesis
    parsed_os = re.findall(r'\(([^()]*)\)', i)
    # List comprehension to get rid of clunky, unwanted characters
    more_parsed_us = [j.strip(' / ') for j in parsed_ua]
    # Append data based on its location
    brow_list.append(more_parsed_us[0:1])
    # Append data based on its location
    browser_ver.append(more_parsed_us[1:2])
    # Append data based on its location
    user_language.append(more_parsed_us[2:3])
    # Append data based on its location
    oper_sys_infras.append(parsed_os)
  # Empty list, yet again, to append information to
  oper_sys_info = []
  # for loop to go through the list we made before
  for i in oper_sys_infras:
    # if a value in the list is not empty
    if len(i) != 0:
      # Apply the function to rid the brackets 
      i = banish_brackets(i)
    # Else if the list is empty
    elif len(i) == 0:
      # Return missing
      i = "Missing"
    # Append the finished loop variable to empty list
    oper_sys_info.append(i)   
  # Assigned the appended list to it's respective column 
  http_frame = http_frame.assign(user_browser = brow_list)
  # Apply further parsing logic
  http_frame['user_browser'] = http_frame['user_browser'].apply(banish_brackets)
  # Assigned the appended list to it's respective column
  http_frame = http_frame.assign(browser_version = browser_ver)
  # Apply further parsing logic
  http_frame['browser_version'] = http_frame['browser_version'].apply(remove_letters)
  # Apply further parsing logic
  http_frame['browser_version'] = http_frame['browser_version'].apply(banish_brackets)
  # Assigned the appended list to it's respective column
  http_frame = http_frame.assign(language_used = user_language)
  # Apply further parsing logic 
  http_frame['language_used'] = http_frame['language_used'].apply(parse_language)
  # Assigned the appended list to it's respective column
  http_frame = http_frame.assign(op_sys_info = oper_sys_info)
  # Out to CSV to acquire the finished frame
  http_frame.to_csv('parsed_http_frame.csv')
  # Return 
  return 
# Import the data
df = pd.read_csv('....Insert path here....')
# If name == main, start the main function
if __name__ == '__main__':
    main()