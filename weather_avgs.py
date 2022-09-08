from Uptown_func import read_csv, newcsv
import numpy as np

data = read_csv('NOAA Files/NOAA_SanJose_CA_2011-2021.csv')

title = data[0]

#get list of days
days = []
for d in data:
    date = d[1]
    date = date.split('/')
    if len(date[0]) == 1:
        date[0] = '0'+date[0]
    if len(date[1]) == 1:
        date[1] = '0'+date[1]
    date = f'{date[0]}/{date[1]}'
    if date not in days:
        days.append(date)
days.sort()

#get average values for list of days
averaged_data = []
for day in days:
    winds, rains, snows, temp_avgs, temp_maxs, temp_mins = [], [], [], [], [], []
    for d in data:
        station, date, avg_wind, rain, snow, snow_depth, temp_avg, temp_max, temp_min = d
        date = date.split('/')
        if len(date[0]) == 1:
            date[0] = '0'+date[0]
        if len(date[1]) == 1:
            date[1] = '0'+date[1]

        date = f'{date[0]}/{date[1]}'

        if date == day:
            if avg_wind != '':
                winds.append(float(avg_wind))
            if rain != '':
                rains.append(float(rain))
            if snow != '':
                snows.append(float(snow))
            if temp_avg != '':
                temp_avgs.append(float(temp_avg))
            if temp_max != '':
                temp_maxs.append(float(temp_max))
            if temp_min != '':
                temp_mins.append(float(temp_min))
#Convert lists to arrays 
    winds, rains, snows, temp_avgs, temp_maxs, temp_mins = np.array(winds), np.array(rains), np.array(snows), np.array(temp_avgs), np.array(temp_maxs), np.array(temp_mins)
#average arrays
    winds, rains, snows, temp_avgs, temp_maxs, temp_mins = np.average(winds), np.average(rains), np.average(snows), np.average(temp_avgs), np.average(temp_maxs), np.average(temp_mins)

    if str(temp_avgs) == 'nan':
        temp_avgs = (temp_maxs + temp_mins)/2
    
    day_data = [day, winds, rains, snows, temp_avgs, temp_maxs, temp_mins]
    print(day_data)
    averaged_data.append(day_data)

#save averaged weather data
title = ['date', 'wind', 'rain', 'snow', 'temp_avg', 'temp_max', 'temp_min']
newcsv('SanJose_CA/SanJose_CA_yearly_averages.csv', title, averaged_data, excel = True)

    
    
