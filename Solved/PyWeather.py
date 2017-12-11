
# coding: utf-8
Summary

The code below attempts to find correlations between a city's relative distance from the equator and that city's weather.  518 random world cities' daily weather attributes were sampled on 2017-12-10.  Scatter plots were created to explore these cities maximum temperature, humidity, cloudiness and wind speed vs that of the city's latitude.

Observations

1.  The closer to the equator (0 degrees latitude), the higher the maximum daily temperatures were on average.  This can be seen by the clear inflection point on the 'World Cities Sample:  Latitude vs Max Temperature on 2017-12-10' plot near 0 degrees latitude.

2.  Cities with the highest daily wind readings tend to be further away from the equator.  In this sample, Kodiak, AK (57.79 latitude) had the highest wind reading at 38.03 mph.

3.  The average humidity for the sample was above 75%.  There does not seem to be a strong correlation between that of humidty and latitude.
# In[79]:

#Initialize Modules
import requests as req
import json
from citipy import citipy as cp
import random
import pandas as pd


# In[88]:

#API setup
api_key = '25bc90a1196e6f153eece0bc0b0fc9eb'
units = 'Imperial'
url = 'http://api.openweathermap.org/data/2.5/weather'


# In[97]:

#Cities Setup - random integers for latitude/longitude
cities_dict = {'city':[],'country':[]}


# In[98]:

#Build City Dictionary
for x in range(0,1500):
	x = cp.nearest_city(random.randint(-90,90), random.randint(-180,180))
	if x.city_name not in cities_dict['city']:
		cities_dict['city'].append(x.city_name)
		cities_dict['country'].append(x.country_code)


# In[99]:

#Check that code is working
for city in cities_dict['city']:
	print(city)

len(cities_dict['city'])


# In[100]:

#Change dict to DataFrame
df_cities = pd.DataFrame.from_dict(cities_dict)
df_cities['lon'] = ''
df_cities['lat']= ''
df_cities['tempF']= ''
df_cities['humidity'] = ''
df_cities['wind_speed'] = ''
df_cities['cloudiness'] = ''

df_cities.head()


# In[102]:

#Building API Call
for index,row in df_cities.iterrows():

	#Set param_dict
	param_dict = {'appid':api_key,
			'units':units, 
			'q': row['city']+','+row['country']
	}
	
	#Get response
	response = req.get(url,params = param_dict)
	print('Processing '+ str(index+1) + ' of ' +str(len(df_cities['city'])) + ' | ' + 
		row['city']+','+row['country'])
	print(response.url)
	data = response.json()
	#print(json.dumps(data,indent=4))
	
	try:
		#Create dictionary key-value pairs
		row['lon'] = data['coord']['lon']
		row['lat'] = data['coord']['lat']
		row['tempF'] = data['main']['temp_max']
		row['humidity'] = data['main']['humidity']
		row['wind_speed'] = data['wind']['speed']
		row['cloudiness'] = data['clouds']['all']
	except:
		continue

#Check Dataframe structure
df_cities.head()


# In[124]:

#Save Data into CSV
df_cities_clean = df_cities.loc[df_cities['lon']!='']
df_cities_clean.to_csv('Cities_Data.csv',index=False)
df_cities_clean.head()


# In[141]:

#Initialize modules for plots
import matplotlib.pyplot as plt
import seaborn as sns


# In[146]:

#Plot Latitude vs Temperature (F) w Latitude being the independent variable

plt.scatter(df_cities_clean['lat'],df_cities_clean['tempF'])
plt.xlabel('Latitude')
plt.ylabel('Maximum Temperature (F)')
plt.title('World Cities Sample:  Latitude vs Max Temperature on 2017-12-10')
plt.xlim(-95,95)
plt.ylim(-65,100)
plt.savefig('Lat_vs_Temp_20171210')
plt.show()


# In[143]:

#Plot Latitude vs Humidity (%) w Latitude being the independent variable

plt.scatter(df_cities_clean['lat'],df_cities_clean['humidity'])
plt.xlabel('Latitude')
plt.ylabel('Humidity (%)')
plt.title('World Cities Sample:  Latitude vs Humidity on 2017-12-10')
#plt.xlim(-95,95)
#plt.ylim(-150,150)
plt.savefig('Lat_vs_Humidity_20171210')
plt.show()


# In[144]:

#Plot Latitude vs Cloudiness (%) w Latitude being the independent variable

plt.scatter(df_cities_clean['lat'],df_cities_clean['cloudiness'])
plt.xlabel('Latitude')
plt.ylabel('Cloudiness (%)')
plt.title('World Cities Sample:  Latitude vs Cloudiness on 2017-12-10')
plt.xlim(-95,95)
#plt.ylim(-150,150)
plt.savefig('Lat_vs_Cloud_20171210')
plt.show()


# In[145]:

#Plot Latitude vs Cloudiness (%) w Latitude being the independent variable

plt.scatter(df_cities_clean['lat'],df_cities_clean['wind_speed'])
plt.xlabel('Latitude')
plt.ylabel('Wind Speed (mph)')
plt.title('World Cities Sample:  Latitude vs Wind Speed on 2017-12-10')
plt.xlim(-95,95)
#plt.ylim(-150,150)
plt.savefig('Lat_vs_Wind_20171210')
plt.show()


# In[ ]:



