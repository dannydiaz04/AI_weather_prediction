from email.headerregistry import Address
import pandas as pd
import numpy as np
from keras.models import load_model
from datetime import date
from datetime import datetime
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, Point
import joblib
import sklearn as sk
import math

# load our model using keras load_model library
weather_loaded_lstm_model = load_model("my_model4.h5")
# load random forest classifier snowfall prediction
snowfall_prediction = joblib.load("random_forest_snow_prediction30.joblib")


'''
Create the tensor. Model takes in the shape (9,9,9). 
We need to have the user input a city, then we need to get the lat/long 
coordinates for that city and input them to the meteostat daily api
and retrieve yesterday's climate numbers. Then we can save that as a tensor and 
feed it into the model. The model will then give us an output tensor. We'll use 
that to disply the next days forecast and as input for the next 6 days.
Final output will be the display of the forecast for the ne
xt seven days. 
'''

# get the previous day's numbers
today = date.today()

# set the date by subtracting 1 from current day
start = datetime(today.year, today.month, today.day - 8)
end = datetime(today.year, today.month, today.day)

''' 
To get lat long we're using the geopy library and Nominatim.
We could use a big dataframe available online, that has zip codes, lat long coords
and city names, but using this library saves lines on code
'''
geolocator = Nominatim(user_agent="my-app")

user_city = input('Enter city: ').lower().strip()
user_country = input('Enter country: ').lower().strip()

if user_country == '':
    address = user_city
    location = geolocator.geocode(address)
else:
    city = user_city
    country = user_country
    location = geolocator.geocode(city+','+ country)
    print("latitude is :-" ,location.latitude,"\nlongtitude is:-" ,location.longitude)

print(location.address)
print((location.latitude, location.longitude))

# set a point that will look for nearby weather stations
point_dummy = Point(location.latitude, location.longitude)

# Get daily data
data = Daily(point_dummy, start, end)
data = data.fetch()

print('''********************************************************************
        \n\nThe last 8 days weather (Temps given in Celcius):
        \n\n********************************************************************
        ''')
print(data)

# get inputs for weather prediction
data_to_use_for_input = data[['tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']]

# check for nan snow values
data['snow'] = data['snow'].fillna(0)

# save inputs for random forest snowfall classifier
data_snowfall_y = np.where(data['snow'] > 0, 1, 0)

# we need to change the wspd and wdir to a vector in radians
wv = data_to_use_for_input.pop('wspd')

# Convert to radians.
wd_rad = data_to_use_for_input.pop('wdir')*np.pi / 180

# Calculate the wind x and y components.
data_to_use_for_input['Wdirx'] = wv*np.cos(wd_rad)
data_to_use_for_input['Wdiry'] = wv*np.sin(wd_rad)

# get the mean for each value so we can replace nan values
mean_values = {
    'tavg': 13.423049192850371,
    'tmin': 9.065401380393482,
    'tmax': 17.64878932049288,
    'prcp': 2.536188545982376,
    'Wdirx': -12.139553430946346,
    'Wdiry': -2.33743324012893,
    'wpgt': 37.60200043056173,
    'pres': 1016.7164620925539,
    'tsun': 376.7633479218932      
}
std_values = { 
'tavg' :    10.665325,
'tmin' :    10.097180,
'tmax' :    11.980711,
'prcp' :     8.648877,
'wpgt' :   14.347446,
'pres' :     6.949505,
'tsun' :   291.500871,
'Wdirx': 9.348482,
'Wdiry' : 7.025097
}

tavg_mean = 13.423049192850371
tavg_std = 10.665325

# initialize the list that will take in input values
input_data_list = np.empty(shape=(9,9))

# create the dataset for the snow fall classifier prediction
# we need a 9,9 array that will give use a 9,1 output of 0's (no snow) or 1's (snow)
for i in data_to_use_for_input.columns:
    j = 0
    while j <= len(data_to_use_for_input[i]) - 1:
        #if value is null, fill it with mean value
        if pd.isna(data_to_use_for_input.iloc[j][i]):
            
            input_data_list[j] = mean_values[i]
        else:    
            input_data_list[j] = data_to_use_for_input.iloc[j][i]
        j += 1


# create the dataset for the rest of the features to feed into the
# neural network. This will be shape 1,9,9
input_data_list_nn = []

for i in data_to_use_for_input.columns:
    #if value is null, fill it with mean value
    if pd.isna(data_to_use_for_input.iloc[0][i]):
            
        input_data_list_nn.append(mean_values[i])
    else:    
        input_data_list_nn.append(data_to_use_for_input.iloc[0][i])

input_data = [[input_data_list_nn]]

input_data_for_snowfall_pred = input_data_list
# input_data_for_snowfall_pred.shape = (81,)



# **********prediction:**********
prediction = weather_loaded_lstm_model.predict(input_data)

denormalized_prediction_output = []

tavg = prediction[0][0][0]*std_values['tavg'] + mean_values['tavg']
tmin = prediction[0][0][1]*std_values['tmin'] + mean_values['tmin']
tmax = prediction[0][0][2]*std_values['tmax'] + mean_values['tmax']
prcp = prediction[0][0][3]*std_values['prcp'] + mean_values['prcp']
wpgt = prediction[0][0][4]*std_values['wpgt'] + mean_values['wpgt']
pres = prediction[0][0][5]*std_values['pres'] + mean_values['pres']
tsun = prediction[0][0][6]*std_values['tsun'] + mean_values['tsun']
Wdirx = prediction[0][0][7]*std_values['Wdirx'] + mean_values['Wdirx']
Wdiry = prediction[0][0][8]*std_values['Wdiry'] + mean_values['Wdiry']

denormalized_prediction_output.append(tavg)
denormalized_prediction_output.append(tmin)
denormalized_prediction_output.append(tmax)
denormalized_prediction_output.append(prcp)
denormalized_prediction_output.append(wpgt)
denormalized_prediction_output.append(pres)
denormalized_prediction_output.append(tsun)
denormalized_prediction_output.append(Wdirx)
denormalized_prediction_output.append(Wdiry)

denormalized_prediction_output_dict = {
    'tavg' : tavg,
    'tmin' : tmin,
    'tmax' : tmax,
    'prcp' : prcp,
    'wpgt' : wpgt,
    'pres' : pres,
    'tsun' : tsun,
    'Wdirx' : Wdirx,
    'Wdiry' : Wdiry,
}

# ****outputs****

print('''\n\n**************************************************************************************)
        \n\nPREDICTION RESULTS BELOW!
        \n\n**************************************************************************************''')

# # fit the classifier
snowfall_prediction.fit(input_data_for_snowfall_pred , data_snowfall_y)
# predict snowfall
# if the list has just one '1', then it will snow, otherwise, it will not
if sum(snowfall_prediction.predict(input_data_for_snowfall_pred)):
    print("\n\nThere will be snowfall tomorrow!!!")
else:
    print("\n\nThere will not be snowfall tomorrow!")


# initialize the output that we'll keep in a list 
final_prediction_of_temps_farenheit = []


final_prediction_of_temps_farenheit.append(round((denormalized_prediction_output_dict['tavg']*(9.0/5.0))+ 32, 0))
final_prediction_of_temps_farenheit.append(round((denormalized_prediction_output_dict['tmin']*(9.0/5.0))+ 32, 0))
final_prediction_of_temps_farenheit.append(round((denormalized_prediction_output_dict['tmax']*(9.0/5.0))+ 32, 0))

print('''\n\n********************\nCelcius Average, Lows, and Highs\n*******************''')
print("\nAverage Temperature (Celcius): " , round(denormalized_prediction_output_dict['tavg'], 1))
print("\nLow Temperature (Celcius): " , round(denormalized_prediction_output_dict['tmin'], 1))
print("\nHigh Temperature (Celcius): " , round(denormalized_prediction_output_dict['tmax'], 1))

print('''\n\n*******************\nFarenheit Average, Lows, and Highs\n*******************''')
print("\nAverage Temperature (Farenheit): ", final_prediction_of_temps_farenheit[0])  
print("\nLow Temperature (Farenheit): ", final_prediction_of_temps_farenheit[1])  
print("\nHigh Temperature (Farenheit): ", final_prediction_of_temps_farenheit[2])  
print("\n\nPrediction of all features: ", denormalized_prediction_output_dict)