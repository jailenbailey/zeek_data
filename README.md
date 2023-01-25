## About
#### This repository is simply a container for some code that I have written to handle and predict on certain types of zeek data. There isn't any data to go along with these scripts/notebooks, as this is simply a repository of scripts for code I wrote during an internship that I might find useful, or someone else might find useful, in the future for Zeek Data. 
#### I will write a short summary for each as follows:

### user_agent_manipulation.ipynb/py
#### This notebook/script was written to handle what parsing libraries I attempted to use could not. As I was attempting to create features of parsed sections of a user agent string for testing, I found that the data I was using was a bit old, and most modern libraries for parsing could not handle the job. So, I took matters into my own hands to attempt this myself through the use of Regular Expressions (REGEX). While I will say the overall solution isn't exactly the most optimal, I find that some of the code may be recyclable/useful in the future. Therefore, I wish to keep it in that case. 

### zeek_data_extraction.py
#### While this is exclusive to log files in JSON format, the data from this code was meant to feed directly into the zeek_xgb_model. I had a small solution inside of the notebook (as it was originally before I converted to a .py script instead), but I found that attempting to gain a whole months worth, 24 files for each day, was taking a considerable amount of time when there could have been an easier solution. So, I decided to dip into a tad of multiprocessing. This will run 4 functions: one for the 01st-09th days, one for the 10th - 19th days, one for the 20th - 29th days, and one for any days starting with 3. Each of these functions will run at the same time, essentially reducing the original 45 minutes it would take (per the size of the files I was dealing with), into just a few minutes. There is likely a better way of doing things, but I found this way to be sufficient for the necessities I needed it for. I will also be pushing an update that also handles gz files that will extract and throw them into a temp folder, leaving the gz files in place. 

### zeeb_xgb_model_minute_intervals.ipynb/py
#### Taking data from the extraction script, this code will parse the times, create features, and predict the future in minute intervals using an XGBoost Regressor. This model is not as efficient in my opinion as the five_minute model or the hourly model, but it could have its place in a certain scenario. 

### zeeb_xgb_model_five_min_intervals.ipynb/py
#### Taking data from the extraction script, this code will parse the times, create features, and predict the future in 5-minute intervals using an XGBoost Regressor. Of the 3 XGBoost models in this repository, this is by far the most efficient.

### zeeb_xgb_model_hourly_intervals.ipynb/py
#### Taking data from the extraction script, this code will parse the times, create features, and predict the future in hourly intervals using an XGBoost Regressor. This model, while not being as efficient as the 5-minute model, is still efficient in it's own way and far more efficient than the minute based model. 