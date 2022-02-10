# Import libaries needed
import pandas as pd
import tensorflow as tf
import requests

# may have to get data from NOAA API. Access token:
#QgOgWlCZcaDPuHKQwhEUxAdPaZrPUyBy

#response = requests.get("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/United%20States?unitGroup=metric&key=JS2FCJWVWHJY5J4TPL48M2TLL&contentType=json")

df = pd.read_json("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/United%20States/2022-01-12?unitGroup=metric&key=JS2FCJWVWHJY5J4TPL48M2TLL&contentType=json")

#df = pd.read_json('D:/CSU\Winter 2021/CSC510 - Foundations of Artificial Intelligence/Portfolio Project/Data/United_States_Test_pulling_dataset.json')


print(df.head)

#print(df.head)


#print(response.json())