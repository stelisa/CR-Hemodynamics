#!usr/bin/python
#coding=utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time

class Blood_pressure():
    
    # inital function
    def __init__(self, csv_file):
        # read blood pressure csv file 
        self.df = pd.read_csv(csv_file)
        
        # get data start year and date
        self.startDate = self.df["time"].iloc[0].split()[0]
        print(self.startDate)
        
        # get data end year and date
        self.endDate = self.df["time"].iloc[-1].split()[0]
        
        # get local time
        self.date = time.strftime("%Y%m%d",time.localtime())
    
    # showhead function is based on pandas function
    def showhead(self, rows):
        # show rows of dataframe    
        print (self.df.head(rows))
        return
    
    # data preprocess function 
    def preprocess(self, name):
        '''
        1. select the columns of interest
        2. eliminate rows when value = -1
        3. adjust 'time' (hours only)
        4. save clean dataframe to csv file with customized name (name)     
        '''
        self.name = name # customized name
        df = self.df[['hr','time','sys','dia']] # select specific columns
        df = df[df.sys != -1] # remove rows by specific 
        df["original_id"] = df.index
        df["time"] = df["time"].apply(lambda x: int(x.split()[1].split(":")[0]))
        df.to_csv('bp_hr/clean/%s_clean.csv'%(name), index=False) # save csv file
        self.clean_csv = pd.read_csv('bp_hr/clean/%s_clean.csv'%(name))
    
    # function of calculation mean of the blood pressure and heart rate 
    def mean_table(self, df = pd.DataFrame(), group = "time", showTable = False, row = 10):
        '''
        1. calculate mean of the blood pressure and the heart rate
        2. return pandas dataframe with group table
        '''
        if df.empty:
            df = self.clean_csv
        table = df.groupby(group)
        if showTable:
            print(table.head(row))
        return table.mean()
    
    # function of calculation stndarf deviation of the blood pressure and the heart rate
    def standard_deviation_table(self, df = pd.DataFrame(), group = "time", showTable = False, row = 10):
        '''
        1. calculate standard deviation of the blood pressure and the heart rate
        2. return pandas dataframe with group table
        '''
        if df.empty:
            df = self.clean_csv
        table = df.groupby(group)
        standardDeviation = table.std()
        if showTable:
            print(standardDeviation.head(row))
        return standardDeviation
        
    #Draw a lineplot: x-axis = hour; y-axis = bp and hr(average sys and dia)
    def lineplot(self, saveFile = False, showImage = True, fileName = "lineplot", title = "24 Hours Blood Pressure Plot"):
        table = self.mean_table() #calculate the mean of each time group
        
        plt.title("%s from %s to %s "%(self.name, self.startDate.replace("-","/"), self.endDate.replace("-","/")) + title)
        plt.plot(table['sys'], label='systolic bp')
        plt.plot(table['dia'], label='diastolic bp')
        plt.plot(table['hr'], label='heart rate')
        plt.legend(loc='lower right', bbox_to_anchor=(1.4, 0.2))
        plt.xlabel('Time(hour)')
        plt.ylabel('mmHg, heart rate/min')
        plt.xticks(np.linspace(0,23,24))
        if saveFile:
            plt.savefig('bp_hr/fig/%s_bp_hr_from_%s_to_%s_%s_%s'%(self.name, self.startDate.replace("-",""), self.endDate.replace("-",""), self.date, fileName), bbox_inches="tight")
        if showImage:
            plt.show()
        plt.clf()
        return
    
        #Draw a lineplot: x-axis = hour; y-axis = bp and hr(average sys and dia)
    def errorbar(self, saveFile = False, showImage = True, fileName = "errorbar", title = "24 Hours Blood Pressure Plot"):
        table = self.mean_table() #calculate the mean of each time group
        standardDeviation = self.standard_deviation_table()
        
        plt.title("%s from %s to %s "%(self.name, self.startDate.replace("-","/"), self.endDate.replace("-","/")) + title)
        plt.errorbar(table.index, table['sys'], yerr = standardDeviation['sys'], label='systolic bp')
        plt.errorbar(table.index, table['dia'], yerr = standardDeviation['dia'], label='diastolic bp')
        plt.errorbar(table.index, table['hr'], yerr = standardDeviation['hr'], label='heart rate')
        plt.legend(loc='lower right', bbox_to_anchor=(1.4, 0.2))
        plt.xlabel('Time(hour)')
        plt.ylabel('mmHg, heart rate/min')
        plt.xticks(np.linspace(0,23,24))
        if saveFile:
            plt.savefig('bp_hr/fig/%s_bp_hr_from_%s_to_%s_%s_%s'%(self.name, self.startDate.replace("-",""), self.endDate.replace("-",""), self.date, fileName), bbox_inches="tight")
        if showImage:
            plt.show()
        plt.clf()
        return