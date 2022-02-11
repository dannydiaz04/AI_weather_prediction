# Import Meteostat library and dependencies
from datetime import datetime
from time import time
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, Point
import pandas as pd


'''
Thoughts
The API only gets data for one location at a time. 
I'm going to have a dtaframe loaded in with all U.S. zipcodes reading 
in their latitude and longitudinal coords then pass that into the Point class.
Then we'll union the entire dataframe to get our historical dataset. If all
goes well, include more zip codes. '''

# read in csv file with all US zipcodes
'''THIS IS THE TEST SET'''
# zips = pd.read_csv(r'D:/CSU/Winter 2021/CSC510 - Foundations of Artificial Intelligence/Portfolio Project/Data/simplemaps_uszips_basicv1.79/uszips_test_code_not_test_set.csv')

# read in csv file with all US zipcodes
'''THIS IS THE REAL ZIPCODE SET'''
zips = pd.read_csv(r'D:/CSU/Winter 2021/CSC510 - Foundations of Artificial Intelligence/Portfolio Project/Data/simplemaps_uszips_basicv1.79/uszips_shuffled_50_zipcode_limit.csv')

#obtain only the latitude and longitude coordinates
zip_coords = zips[['lat', 'lng', 'city', 'state_name']]

# Set time period
start = datetime(1980, 1, 1)
end = datetime(2021, 12, 31)


# using the python itertuples method, iterate over both columns
for lat, lng, city, state_name in zip_coords.itertuples(index=False):

    # initialize the dataframe every time
    new_df = pd.DataFrame()

    #set a point that will look for nearby weather stations
    point_dummy = Point(lat, lng)

    # Get daily data
    data = Daily(point_dummy, start, end)
    data = data.fetch()

    # concat dataframes
    new_df = new_df.append(data)
    new_df['lat'] = lat
    new_df['lng'] = lng
    new_df['city'] = city
    new_df['state_name'] = state_name

    
    if new_df.empty:
        pass
    else:
        new_df.to_csv('D:/CSU/Winter 2021/CSC510 - Foundations of Artificial Intelligence/Portfolio Project/Data/simplemaps_uszips_basicv1.79/climate_data_for_US/hist_data' + str(lat)+ str(lng) + '.csv')


print("ALL DONE")