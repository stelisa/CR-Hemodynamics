# !usr/bin/python
# coding=utf-8
'''
This script is for analyzing the dash blood pressure data and 
draw heatmap to map the period of sleep and awake.
'''
# import essential packages
import pandas as pd
import numpy as np
import dash_analysis_toolbox as dt

# read abpm_d2.csv file
df = pd.read_csv('abpm_d2.csv')
# subset the columns we need
df = df[['ID_REL', 'DIET', 'SBP', 'DBP', 'TIME', 'SODIUM','SLEEPFRO','SLEEPTO']]


# Adjust the time, replace the value in the column by hour
df['TIME'] = df['TIME'].apply(dt.timechange)
df['SLEEPFRO'] = df['SLEEPFRO'].apply(dt.timechange)
df['SLEEPTO'] = df['SLEEPTO'].apply(dt.timechange)


# iterate from the time column
for i in range(len(df['SLEEPFRO'])): 
    # avoid some value present 0 as 0 O'clock, here we add 24 to zero
    if df['SLEEPFRO'][i] == 0:
        df['SLEEPFRO'][i] += 24
    elif df['SLEEPTO'][i] == 0:
        df['SLEEPTO'][i] += 24


# if sleepto value is smaller than sleepfro, neet to add 24
for i in range(len(df['SLEEPFRO'])):
	if df['SLEEPTO'][i] < df['SLEEPFRO'][i]:
		df['SLEEPTO'][i] += 24  

df.to_csv('abpm_dash.csv')

# Step3. Seperate to two diet group: dash and combination
# Seperate to three more group H, M, L
df_new = pd.read_csv('abpm_dash.csv')

H_dash=[]; M_dash=[]; L_dash=[]
H_control=[]; M_control=[]; L_control=[]

for x in range(len(df_new["DIET"])):
    if df_new['DIET'][x] == "COMBINATION": #如果 DIET 那欄的值是 COMBINATION 則將 index 加到 dash
        if df_new['SODIUM'][x] == 'H':
            H_dash.append(x)
        elif df_new['SODIUM'][x] == 'M':
            M_dash.append(x)
        else:
            L_dash.append(x) 

    else:
        if df_new['SODIUM'][x] == 'H':
            H_control.append(x)
        elif df_new['SODIUM'][x] == 'M':
            M_control.append(x)
        else:
            L_control.append(x) 

df_new.loc[H_dash].to_csv('H_dash.csv')
df_new.loc[M_dash].to_csv('M_dash.csv')
df_new.loc[L_dash].to_csv('L_dash.csv')
df_new.loc[H_control].to_csv('H_control.csv')
df_new.loc[M_control].to_csv('M_control.csv')
df_new.loc[L_control].to_csv('L_control.csv')


# use self-write function to draw heatmap and save it
import PIL # for figure format
import dash_analysis_toolbox as dat

dat.heatmap() # follow the pop-out instruction
