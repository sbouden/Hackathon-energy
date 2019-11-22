#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import datetime
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

API_KEY="176d44eb0b0047b08d19c62b252313ad"
website_forecast = "https://api.weatherbit.io/v2.0/forecast/hourly?city="
website_historical="https://api.weatherbit.io/v2.0/history/hourly?city="
city_name="Toulouse"
start_date="17-11-22"
nb_days=3

#x=open('resJson.txt', 'r').read()
#res = json.loads(x)

def getX_dataFrame(jsonObj):
    col=[]
    data=jsonObj['data']
    for d in data:
        col.append([d['timestamp_local'][-8:], d['temp'], d['wind_spd'], d['clouds']])

    df = pd.DataFrame(col, columns = ['time', 'temp', 'wind', 'clouds'])
    return df

def getHistoricalDataFrame(city_name, start_date, nb_days):
    data=[]
    df=pd.DataFrame(data, columns = ['time', 'temp', 'wind', 'clouds'])
    start_date = datetime.datetime.strptime(start_date, "%y-%m-%d")
    for i in range(nb_days):
        end_date = start_date + datetime.timedelta(days=1)
    
        start_date = start_date.strftime("%y-%m-%d")
        end_date = end_date.strftime("%y-%m-%d")
    
        print("getting data from " + start_date + " to " + end_date)
        res_string = website_historical + city_name + "&start_date=20"+start_date+"&end_date=20"+ end_date +"&tz=local&key="+API_KEY
        res = requests.get(res_string).json()
        df_temp = getX_dataFrame(res)
        df = pd.concat([df, df_temp])
        
        start_date = datetime.datetime.strptime(end_date, "%y-%m-%d")
        time.sleep(1)
    return df

def getForcastDataFrame(city_name):
    res = requests.get(website_forecast + city_name + "&key=" +API_KEY+ "&hours=48").json()
    return getX_dataFrame(res)

#df = getHistoricalDataFrame(city_name, start_date, nb_days)
df = pd.read_csv("data_weather.csv") 
#df.to_csv('data_weather.csv')
X=df[['time', 'temp', 'wind', 'clouds']]
Y=df_Guillaume['conso']

X_train, X_test = train_test_split(X, test_size=0.2)
Y_train, Y_test = train_test_split(Y, test_size=0.2)

reg = LinearRegression(fit_intercept=True).fit(X_train, Y_train)
Y_pred = reg.predict(X_test)

M=np.ones(len(Y_test))*Y_test.mean()
v1=(Y_pred-M)
nominateur=np.dot(v1,v1)
v2=(Y_test-M)
denominateur=np.dot(v2,v2)
R2=nominateur/denominateur
print("Coefficient de détermination du modèle combiné: R2=%f" % R2)

X_forecast=getForcastDataFrame(city_name)
Y_forecast = reg.predict(X_forecast)
print("Consommation prévue:")
print(Y_forecast)