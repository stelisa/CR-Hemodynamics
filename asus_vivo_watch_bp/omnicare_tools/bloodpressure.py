#!usr/bin/python
#coding=utf-8
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time

class Blood_pressure():
    
    def __init__(self, csv_file):
        # initial function
        # read blood pressure csv file download from OmniCare website 
        self.df = pd.read_csv(csv_file)
        
        # get data start year and date
        self.startDate = self.df["time"].iloc[0].split()[0]
        
        # get data end year and date
        self.endDate = self.df["time"].iloc[-1].split()[0]
        
        # get local time
        self.date = time.strftime("%Y%m%d",time.localtime())
    
    
    def showhead(self, rows):
        # This function is based on pandas .head() function
        # show rows of dataframe, input arbitary row number    
        df = self.df.head(rows) 
        print (df)
    
     
    def preprocess(self,name): 
        '''
        Save and manipulate data we are interested and save it to a csv file.
        Input: bp_hr/raw/blood_pressure.csv download from OmniCare website
        Output: save the cleaned.csv file in /bp_hr/clean 
        '''
        self.name = name # customized name
        df = self.df[['hr','time','sys','dia']] # select specific interest columns
        df = df[df.sys != -1] # remove rows when value = -1 
        df["original_id"] = df.index # reset index
        df["time"] = df["time"].apply(lambda x: int(x.split()[1].split(":")[0])) # adjust 'time' (hours only)
        df.to_csv('bp_hr/clean/%s_clean.csv'%(name), index=False) # save cleaned.csv file
        self.clean_csv = pd.read_csv('bp_hr/clean/%s_clean.csv'%(name))
        
    def mean_table(self, df = pd.DataFrame(), group = "time", showTable = False, row = 10):
        '''
        Calculate mean blood pressure and heart rate of preprocess() output
        Input: preprocess() output
        Output: return pandas dataframe with mean blood pressure & heart rate by group 
        '''
        if df.empty:               # if df is empty (no input), then it will take the output of preprocess() 
            df = self.clean_csv
        table = df.groupby(group)  
        if showTable:              # showTable = True
            print(table.head(row))
        return table.mean()
    
    def standard_deviation_table(self, df = pd.DataFrame(), group = "time", showTable = False, row = 10):
        '''
        Calculate standard deviation (std) of blood pressure and heart rate
        Input: preprocess() output
        Output: return pandas dataframe with std of blood pressure & heart rate by group
        '''
        if df.empty:
            df = self.clean_csv
        table = df.groupby(group)
        standardDeviation = table.std()
        if showTable:
            print(standardDeviation.head(row))
        return standardDeviation
        
    def lineplot(self, saveFile = False, showImage = True, fileName = "lineplot", title = "24 Hours Blood Pressure Plot"):
        '''
        lineplot; x-axis = hour; y-axis = bp and hr (average sys and dia); with figure lengend
        Input: preprocess() output
        Output: bp_hr/.png figure file
        '''
        table = self.mean_table() #calculate the mean of each time group
        #print(table['hr']) #you can print a single column
        
        plt.title("%s from %s to %s "%(self.name, self.startDate.replace("-","/"), self.endDate.replace("-","/")) + title)
        plt.plot(table['sys'], label='systolic bp')
        plt.plot(table['dia'], label='diastolic bp')
        plt.plot(table['hr'], label='heart rate')
        plt.legend(loc='lower right', bbox_to_anchor=(1.4, 0.2))
        plt.xlabel('Time(hour)')
        plt.ylabel('mmHg, heart rate/min')
        plt.xticks(np.linspace(0,23,24))
        if saveFile:
            plt.savefig('bp_hr/fig/%s_bp_hr_from_%s_to_%s_%s_%s'%(self.name,
                                                                  self.startDate.replace("-",""),
                                                                  self.endDate.replace("-",""),
                                                                  self.date, fileName), bbox_inches="tight")
        if showImage:
            plt.show()
        plt.clf() # clean the figure
        return
 
    def errorbar(self, saveFile = False, showImage = True, fileName = "errorbar", title = "24 Hours Blood Pressure Plot"):
        '''
        lineplot with errorbar; x-axis = hour; y-axis = bp and hr (average sys and dia); with figure legend
        Input: preprocess() output
        Output: bp_hr/.png figure file
        '''
        table = self.mean_table() #calculate the mean in each time group
        standardDeviation = self.standard_deviation_table() #calcualte the std in each time group
        #print(table['hr']) #you can print a single column

        plt.title("%s from %s to %s "%(self.name, self.startDate.replace("-","/"), self.endDate.replace("-","/")) + title)
        plt.errorbar(table.index, table['sys'], yerr = standardDeviation['sys'], label='systolic bp')
        plt.errorbar(table.index, table['dia'], yerr = standardDeviation['dia'], label='diastolic bp')
        plt.errorbar(table.index, table['hr'], yerr = standardDeviation['hr'], label='heart rate')
        plt.legend(loc='lower right', bbox_to_anchor=(1.4, 0.2))
        plt.xlabel('Time(hour)')
        plt.ylabel('mmHg, heart rate/min')
        plt.xticks(np.linspace(0,23,24))
        if saveFile:
            plt.savefig('bp_hr/fig/%s_bp_hr_from_%s_to_%s_%s_%s'%(self.name,
                                                                  self.startDate.replace("-",""),
                                                                  self.endDate.replace("-",""),
                                                                  self.date, fileName), bbox_inches="tight")
        if showImage:
            plt.show()
        plt.clf() # clean the figure
        return