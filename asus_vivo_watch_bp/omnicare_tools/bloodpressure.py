#!usr/bin/python
#coding=utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Blood_pressure():
    
    #1
    def __init__(self, csv_file):
        # read blood pressure csv file 
        self.df = pd.read_csv(csv_file)
    
    #2
    def showhead(self, rows):
        # show rows of dataframe    
        df = self.df.head(rows)
        print (df)
    
    #3
    def preprocess(self,name):
        '''
        1. select the columns of interest
        2. eliminate rows when value = -1
        3. adjust 'time' (hours only)
        4. save clean dataframe to csv file with customized name (name)     
        '''
        self.name = name # customized name
        df = self.df[['hr','time','sys','dia']] # select specific columns
        df = df[df.sys != -1] # remove rows by specific value
        
        def time_delete_year(t):
            (y,hm) = t.split() # split year and hour:minute:second
            result = hm # return only hour:minute:second
            return result
        
        def time_delete_minute(t):
            (h,m,s) = t.split(':') # split data by colon ':'
            result = int(h) # return only hour
            return result
        
        df['time'] = df['time'].apply(time_delete_year).apply(time_delete_minute) # adjust time to hour
        df.to_csv('%s_clean.csv'%(name)) # save csv file