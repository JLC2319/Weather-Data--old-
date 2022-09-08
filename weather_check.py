from Uptown_func import read_csv

data = read_csv('Atlanta_GA/Atlanta_GA_yearly_averages.csv')

start = '01/01'
end = '07/30'

#Index start and end ranges
for d in data:
    if start == d[0]:
        alpha = data.index(d)
    if end == d[0]:
        omega = data.index(d)+1
#establish list of days within range
days = []
for i in range(alpha, omega):
    day = data[i]
    days.append(day)

#establish ranges
min_snow = .05
low_temp, high_temp = 35, 95

#determine days out of workable ranges
baddays = 0
for day in days:
    date,wind,rain,snow,temp_avg,temp_max,temp_min = day
    
    snow, temp_max, temp_min = float(snow), float(temp_max), float(temp_min)
    
    if temp_max > high_temp or temp_min < low_temp or snow > min_snow:
        baddays += 1

#Outputs
numdays = omega - alpha
percent_bad = int((baddays/numdays)*100)
Margin_of_safety = 20
sched_adjust = int(percent_bad*(1+(Margin_of_safety/100)))

#Print outputs
print(f'\nChecking Dates between {start} & {end}\n')
print(f'\tTotal Days Reviewing: {numdays}')
print(f'\tDays Out of Ranges: {baddays}')
print(f'\tPercent out of Ranges: {percent_bad}%\n')
print(f'Reccomended Workday Multiplier: {sched_adjust}%')
print(f'\t*{Margin_of_safety}% Margin of Safety')