from pymongo import MongoClient
import pandas as pd
from selenium import webdriver
import pandas as pd
import time
import glob
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import TEXT
import re
import numpy as np 

#Change path to the folder with all csv files
directory = '/Users/zinebbenameur/Desktop/Desktop - MacBook Pro/Fasoc/filesall/*.csv'
#directory = '/Users/zinebbenameur/Desktop/Desktop - MacBook Pro/Fasoc/filesall/*.csv'
client = MongoClient()
#specify the name of the database
db=client.config
#specify the name of the collection, here my collection is "test2"
Digikey_py = db.digikey_transformed


#Ppython program to check if two  
# to get unique values from list 
# using numpy.unique  

  
# function to get unique values 
def unique(list1): 
    x = np.array(list1) 
    print(np.unique(x)) 

i = 0

for filename in glob.glob(directory):
    #print("------------", filename , "------------------")
    i = i+1
    df = pd.read_csv(filename) #csv file which you want to import
    #print("replacing . by , in " , filename )
    df.columns = df.columns.str.replace(r"[.]", ",")
    #find columns containing current
    colNames_current = [col for col in df.columns if 'Current -' in col]
    colNames_voltage = [col for col in df.columns if 'Voltage -' in col]
    colNames_temp = [col for col in df.columns if 'Temperature' in col]
    colNames_band = [col for col in df.columns if 'Gain Bandwidth Product' in col]
    colNames_freq = [col for col in df.columns if 'Frequency' in col]
    print('colNames_voltage', colNames_voltage)  
    print('colNames_current', colNames_current)    

    try:  
        df = df.drop(["Quantity Available","Factory Stock", "@ qty","Minimum Quantity" ], axis=1)    
        #Change to path to the folder with all csv files
        start = '/Users/zinebbenameur/Desktop/Desktop - MacBook Pro/Fasoc/filesall/'
        end = '_'
        #Add new subcategory column in the csv
        subcategory = filename[filename.find(start)+len(start):filename.rfind(end)]
        
        
        #subcategory = filename.split('_')[1]
        df['Category'] = "IC"
        df['Subcategory'] = subcategory     
        if 'Operating Temperature' in df.columns:
            #print("----- Split temperature------",i)
            df[['min Operating Temp (°C)','max Operating Temp (°C)']] = df['Operating Temperature'].str.split('~',expand=True,)
            df['min Operating Temp (°C)'] = df['min Operating Temp (°C)'].str.replace("°C", "")
            df['max Operating Temp (°C)'] = df['max Operating Temp (°C)'].str.replace("°C", "")
            df['max Operating Temp (°C)'] = df['max Operating Temp (°C)'].str.replace(r"\(.*\)","")
            df = df.drop(["Operating Temperature"], axis=1)

        if 'Sensing Temperature' in df.columns:
            #print("----- Split temperature------",i)
            df[['min Sensing Temp (°C)','max Sensing Temp (°C)']] = df['Sensing Temperature'].str.split('~', n = 1, expand=True,)
            df['min Sensing Temp (°C)'] = df['min Sensing Temp (°C)'].str.replace("°C", "")
            df['max Sensing Temp (°C)'] = df['max Sensing Temp (°C)'].str.replace("°C", "")
            df['max Sensing Temp (°C)'] = df['max Sensing Temp (°C)'].str.replace(r"\(.*\)","")
            df = df.drop(["Sensing Temperature"], axis=1)


        if 'Voltage - Supply' in df.columns:            
            #print("------Split supply voltage")
            df[['min Voltage - Supply (V)','max Voltage - Supply (V)']] = df['Voltage - Supply'].str.split('~', n = 1, expand=True,)
            df['min Voltage - Supply (V)'] = df['min Voltage - Supply (V)'].str.replace("V", "")
            df['max Voltage - Supply (V)'] = df['max Voltage - Supply (V)'].str.replace("V", "")
            df = df.drop(["Voltage - Supply"], axis=1)

        if 'Voltage - Supply, Single/Dual (±)' in df.columns:
            df[['min Voltage - Supply (V)','max Voltage - Supply (V)']] = df['Voltage - Supply, Single/Dual (±)'].str.split('~', n = 1, expand=True,)
            df['min Voltage - Supply (V)'] = df['min Voltage - Supply (V)'].str.split('V').str[0]
            df['max Voltage - Supply (V)'] = df['max Voltage - Supply (V)'].str.split('V').str[0]
            df['min Voltage - Supply (V)'] = df['min Voltage - Supply (V)'].str.replace("V", "")
            df['max Voltage - Supply (V)'] = df['max Voltage - Supply (V)'].str.replace("V", "")
            df = df.drop(["Voltage - Supply, Single/Dual (±)"], axis=1)
            

        if 'Slew Rate' in df.columns:
           df['Slew Rate (V/µs)'] = df['Slew Rate'].str.replace("V/µs", "")
           df = df.drop(["Slew Rate"], axis=1)

        if 'Temperature Coefficient (Typ)' in df.columns:
            df['Temperature Coefficient (Typ) (ppm/°C)'] = df['Temperature Coefficient (Typ)'].str.split('ppm/°C').str[0]
            df = df.drop(["Temperature Coefficient (Typ)"], axis=1)

        if 'Temperature Coefficient' in df.columns:
            df['Temperature Coefficient (ppm/°C)'] = df['Temperature Coefficient'].str.split('ppm/°C').str[0]
            df = df.drop(["Temperature Coefficient"], axis=1)

        try:
            for elm in colNames_freq:
                print("I enter the for loop for : ", str(elm))
                if str(elm) in str(df.columns) :
                    print("elm is in df.columns", str(elm))
                    for k in range(len(df[str(elm)])):
                        if df[str(elm)][k] != "-":
                            res = re.findall('(\d+|\D+)', df[str(elm)][k])
                            j = len(res)
                            if str(res[j-1]) == "kHz":
                                print("case where unit is kHz")
                                unit = str(res[j-1])
                                df[str(elm)][k] = 0.001 * float(str(df[str(elm)][k]).replace(unit, ''))
                            elif str(res[j-1]) == "MHz":
                                print("case where unit is MHz")
                                unit = str(res[j-1])
                                df.at[k,str(elm)] = str(df[str(elm)][k]).replace(unit, '')
                            else:
                                print("SOMETHING DIFFERENT")
                    df.rename({str(elm): str(elm) + ' (MHz)'}, axis=1, inplace=True)              
                else:
                    continue
        except:
            print("warning something wrong")
            pass     
        try:
            for elm in colNames_band :
                print("I enter the for loop for : ", str(elm))
                if str(elm) in str(df.columns) :
                    print("elm is in df.columns", str(elm))
                    for k in range(len(df[str(elm)])):
                        if df[str(elm)][k] != "-":
                            res = re.findall('(\d+|\D+)', df[str(elm)][k])
                            j = len(res)
                            if str(res[j-1]) == "kHz":
                                print("case where unit is kHz")
                                unit = str(res[j-1])
                                df[str(elm)][k] = 0.001 * float(str(df[str(elm)][k]).replace(unit, ''))
                            elif str(res[j-1]) == "MHz":
                                print("case where unit is MHz")
                                unit = str(res[j-1])
                                df.at[k,str(elm)] = str(df[str(elm)][k]).replace(unit, '')
                            else:
                                print("SOMETHING DIFFERENT")
                    df.rename({str(elm): str(elm) + ' (MHz)'}, axis=1, inplace=True)              
                else:
                    continue
        except:
            pass
        print("************ENTER CURRENT*******")
        print (" STRING ELEMENY", elm)        
        try:
            for elm in colNames_current:
                print("I enter the for loop for : ", str(elm))
                if str(elm) in str(df.columns) :
                    print("elm is in df.columns", str(elm))
                    for k in range(len(df[str(elm)])):
                        if df[str(elm)][k] != "Adjustable" and df[str(elm)][k] != "-":
                            res = re.findall('(\d+|\D+)', df[str(elm)][k])
                            j = len(res)
                            if str(res[j-1]) == "µA":
                                print("case where unit is µA")
                                unit = str(res[j-1])
                                df[str(elm)][k] = 0.001 * float(str(df[str(elm)][k]).replace(unit, ''))
                                print("NEW VALUE   : ", df[str(elm)][k] )
                            elif str(res[j-1]) == "A":   
                                print("case where unit is A")
                                unit = str(res[j-1])                    
                                df.at[k,str(elm)] = 1000 * float(str(df[str(elm)][k]).replace(unit, ''))
                                print("NEW VALUE   : ", df[str(elm)][k] )
                            elif str(res[j-1]) == "pA":   
                                print("case where unit is pA")
                                unit = str(res[j-1])                    
                                df.at[k,str(elm)] = 1e-9 * float(str(df[str(elm)][k]).replace(unit, ''))
                                print("NEW VALUE   : ", df[str(elm)][k] )
                            elif str(res[j-1]) == "mA":
                                print("case where unit is mA")
                                print("old value", df[str(elm)][k])
                                unit = str(res[j-1])
                                print("test", df[str(elm)][k])                            
                                df.at[k,str(elm)] = str(df[str(elm)][k]).replace(unit, '')
                            elif str(res[j-1]) == "nA":
                                print("case where unit is nA")
                                unit = str(res[j-1])
                                df[str(elm)][k] = 0.0000010 * float(str(df[str(elm)][k]).replace(unit, ''))
                                print("NEW VALUE   : ", df[str(elm)][k] )
                            else:
                                print("SOMETHING DIFFERENT")
                    df.rename({str(elm): str(elm) + ' (mA)'}, axis=1, inplace=True)               
                else:
                    continue
        except:
            pass
        try:        
            for elm in colNames_voltage:
                print("I enter the for loop for : ", str(elm))
                if str(elm) in str(df.columns) and (str(elm) != 'Voltage - Supply' or  str(elm) != 'Voltage - Supply, Single/Dual (±)'):
                    print("elm is in df.columns", str(elm))
                    for k in range(len(df[str(elm)])):
                        print("value of k", k)
                        print('Part number', df['Digi-Key Part Number'][k])
                        print("SPLITTING this", df[str(elm)][k])
                        if df[str(elm)][k] != "-":
                            print("not - ")
                            res = re.findall('(\d+|\D+)', df[str(elm)][k])
                            j = len(res)                   
                            print("*****RESULT*****", str(res))
                            if str(res[j-1]) == "V":
                                print("case where unit is V")
                                print("old value", df[str(elm)][k])
                                unit = str(res[j-1])
                                print("test", df[str(elm)][k])                            
                                df.at[k,str(elm)] = str(df[str(elm)][k]).replace(unit, '')
                                print("NEW VALUE   : ", df[str(elm)][k])
                            elif str(res[j-1]) == "mV":
                                print("case where unit is mV")
                                print("old value", df[str(elm)][k])
                                unit = str(res[j-1])
                                print("test", df[str(elm)][k])                            
                                df.at[k,str(elm)] = 0.001 * float(str(df[str(elm)][k]).replace(unit, ''))
    
                            elif str(res[j-1]) == "µV":
                                print("case where unit is µV")
                                print("old value", df[str(elm)][k])
                                unit = str(res[j-1])
                                print("test", df[str(elm)][k])                            
                                df.at[k,str(elm)] = 1e-6 * float(str(df[str(elm)][k]).replace(unit, ''))
                        
                            elif str(res[j-1]) == "nV":
                                print("case where unit is nV")
                                unit = str(res[j-1])
                                print("test", df[str(elm)][k])                            
                                df.at[k,str(elm)] = 1.0E-9 * float(str(df[str(elm)][k]).replace(unit, ''))
                        
                        
                            else:
                                print("SOMETHING DIFFERENT")
                    df.rename({str(elm): str(elm) + ' (V)'}, axis=1, inplace=True)        
                else:
                    continue
        except:
            pass

        #change units in place
        #df['Discounted_Price'] = df['Cost'] - (0.1 * df['Cost']) 
        #Delete all element we don't need from the csv files
        #print("----- Delete all element we don't need from the csv files------",i)
        #df.columns = df.columns.str.replace("[.]", ",")
    except:
        pass


    #Insert record in the DB
    Digikey_py.insert_many(df.to_dict('records'), bypass_document_validation=True)
    db.digikey_transformed.create_index('Unit Price (USD)')

print("----- TOTAL NUMBER OF CSV modified and inserted------",i)