#Author:Sunshin Kim (sunshinkim3@gmail.com)
# Krishna(krishdb38@gmail.com)

import pandas as pd
import numpy as np
import os
import subprocess
import time
import os
import sys
from scipy import stats
import shutil  # To copy parameter File from test to testing Folder
#from shutil import copyfile
# Declaring Global Variables
print("Welcome To FF Analysis 1.0 Version.......TESTING....")
print("Prototype Developed By Sunshin Kim (sunshinkim3@gmail.com) ")
print("Code updated by Adh Krish krishdb38@gmail.com \n")

read_bin_info = None  # User Input Read Bin File
ffy_read = None       # FFyread + ... Out put By Loesstrain() Function
t_read = None  # t_read +.... is  also Output By Loesstrain() Function
temptrain_read_y = None  # output By Enet() Function Arrangetrain()
temptrain_read_rf = None  # Output By Enet() Function
temp_train_par_read = "temptrain_par_read.csv"  # 1000 Data Set
#temp_train_par_read =None#Output By GLmnet for Training Purpose
enet_read = None  # Output By testing cal_enetread

# Global Variable for RL
rl_bin_info = None  # User Input RL Bin File
ffy_rl = None       # FFyread + ... Out put By Loesstrain() Functio  = None       #tread +.... is  also Output By Loesstrain() Function
t_rl = None  # tread +.... is  also Output By Loesstrain() Function
temptrain_rl = None  # Output by Arrangetrain()
temptrain_rl_y = None  # output By Enet() Function
temptrain_rl_rf = None  # Output By Enet() Function
enet_rl = None

temp_train_par_rl = "temptrain_par_rl.csv"
#temp_train_par_rl =None #Output By GLmnet for Training Purpose


def read_bin():
    global rl_bin_info, read_bin_info   # info File

    global ffy_read, t_read
    global ffy_rl, t_rl
    global temptrain_rl_rf, temptrain_rl_y
    global temptrain_rc_rf, temptrain_rc_y
    #Parameter Value
    #global temp_train_par_read , temp_train_par_rl
    global enet_read, enet_rl
    
    files = os.listdir("./testing/")
    #print(files)
    for file in files:
        if file[:8] == "read_bin":
            read_bin_info = file
            ffy_read = "ffy_read_"+file[13:]
            t_read = "t_read_" + file[13:]
            temptrain_read_rf = "temptrain_read_rf"+file[13:]
            temptrain_read_y = "temptrain_read_y"+file[13:]
            #temp_train_par_read = "temptrain_par_read"+file[13:]
            enet_read = "enet_read_" + file[13:]
    if read_bin_info == None:
        print("Read Bininfo file Not found")
        sys.exit(1)
    #for RL
    files = os.listdir("./testing/")
    for file in files:
        if file[:6] == "rl_bin":
            rl_bin_info = file
            ffy_rl = "ffy_rl_"+file[11:]
            t_rl = "t_rl_" + file[11:]

            temptrain_rl_rf = "temptrain_rl_rf_"+file[1:]
            temptrain_rl_y = "temptrain_rl_y_"+file[11:]
            #temp_train_par_rl = "temptrain_par_rl"+file[11:]
            enet_rl = "enet_rl_"+file[11:]

    if rl_bin_info == None:
        print("RL Bininfo file Not found")
        sys.exit(1)
    files = os.listdir("./")
    print("we found following Read and RL bininfo files")
    print("Read info file is \t", read_bin_info)
    print("RL info file is \t", rl_bin_info)


def get_parameter_file():  # Files must be copoied by Automatic....py
    global temp_train_par_rc, temp_train_par_rl
    files = os.listdir("./training/")

    if temp_train_par_rc in files and temp_train_par_rl in files:
        shutil.copy("./training/"+temp_train_par_rc, "./testing/")
        shutil.copy("./training/"+temp_train_par_rl, "./testing/")
        print("Files Copied SUCCESSFULLY")
    else:
        print("Please Copy temptrain parameter Files Manually")
        print("In the Absence of Parameter Files Cant predict Output")

##################### Read Function ###################


def Loesstest_read():  # Rscript Code Will Run with Python
    global read_bin_info, ffy_read, t_read
    os.chdir("./testing/")  # changed the working Directory
    cmd = ['Rscript', 'loessgctest.R', read_bin_info, ffy_read, t_read]
    #Parameter Must be passed bininfo file, Y and X[ffyread and t read is Output file made by loessgctrain.R]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(out.stderr) if out.stdout else print(
        out.stdout, "cal_enet of read. Ran SuccessFully")
    print("loess gct test Read Run Success")


def Arrangetest_read():
    global ffy_read, t_read, temptrain_read_y, temptrain_read_rf
    df_y = pd.read_csv(ffy_read, usecols=[1])
    df_y = df_y.rename(columns=df_y.iloc[0])  # Rename First Row as Header
    # Since Header is replaced with FIrst Row so remove FIrst Row
    df_y = df_y.iloc[1:, :]
    # ,index = None , header = False)
    df_y.to_csv(temptrain_read_y, index=False)
    #Variable Y
    df_x = pd.read_csv(t_read)
    df_x = df_x.iloc[:, 1:]
    df_x = df_x.rename(columns=df_x.iloc[0])
    df_x = df_x.iloc[1:, :]
    df_x.to_csv(temptrain_read_rf, index=None)
    print("Temp test read y and rf(x) Created Successfully")


def cal_enet_read():
    print("Calculating calenet_Read")
    global temp_train_par_read, temptrain_read_y, temptrain_read_rf, enet_read
    #print(type(temp_train_par_read) , type(temptrain_read_y) , type(temptrain_read_rf) ,type(enet_read))
    #Accept 3 Parameter as input and Give One Output enet.read
    #Cal_enet  first param temptrain_par_read_.. , temp_test_read_y_.. ,temp_test_read_rf(x).. and Output_file to save

    cmd = ['Rscript', 'cal_enetrc.R', temp_train_par_rc,
           temptrain_rc_y, temptrain_rc_rf, enet_rc]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(out.stderr) if out.stderr else print(out.stdout)
    

####################### RL Function   #################


def rlnormtest():  # rlnormtest change
    global rl_bin_info, ffy_rl, t_rl
    cmd = ['Rscript', "rlnormtest.R", rl_bin_info, ffy_rl, t_rl]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(out.stderr) if out.stderr else print(out.stdout)


def Arrangetest_rl():
    global ffy_rl, t_rl, temptrain_rl, temptrain_rl_rf, temptrain_rl_y
    df_y = pd.read_csv(ffy_rl, usecols=[1])
    df_y = df_y.rename(columns=df_y.iloc[0])  # Rename First Row as Header
    df_y = df_y.iloc[1:, :]  # Remove First Rows
    df_y.to_csv(temptrain_rl_y, index=False)  # save as csv

    df_x = pd.read_csv(t_rl)
    df_x = df_x.iloc[:, 1:]
    df_x = df_x.rename(columns=df_x.iloc[0])
    df_x = df_x.iloc[1:, :]
    df_x.to_csv(temptrain_rl_rf, index=False)
    merge = pd.concat([df_y, df_x], axis=1)
    merge.to_csv(temptrain_rl)
    print("arrange test_rl Finished")


def cal_enet_rl():
    global temp_train_par_rl, temptrain_rl_y, temptrain_rl_rf, enet_rl

    cmd = ['Rscript', 'cal_enetrl.R', temp_train_par_rl,
           temptrain_rl_y, temptrain_rl_rf, enet_rl]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(out.stderr) if out.stderr else print(out.stdout)


def Cal_Cor():
    global enet_read, enet_rl
    df1 = pd.read_csv(enet_rl, usecols=["final_enet"])
    df2 = pd.read_csv(enet_rc, usecols=["final_enet", "V1"])
    df1 = pd.concat([df1, df2], axis=1)
    #Renaming The Column Name to Avoid Conflict
    df1.columns = ['final_enet', 'final_enet_1', 'Standard FF']
    # Creating Average of Both
    df1["Predicted"] = (df1["final_enet"]+df1["final_enet_1"])/2
    df1 = df1.iloc[:, 2:]
    Correlation = stats.pearsonr(df1["Standard FF"], df1.Predicted)[
        0]  # Calculating Correlation
    df1 = df1.append(
        pd.Series(["Correlation", Correlation], index=df1.columns), ignore_index=True)
    df1.to_csv("Correlation_Result.csv", sep="\t")
    print("The Co relation is ",Correlation)
    print("Corelation is also saved in your csv file buttom")
    print("If You have any Problem Please mail us")
    print("Thank You......")


if __name__ == "__main__":
    read_bin()
    get_parameter_file() #On
    Loesstest_read() #Run RL Norm test
    #os.chdir("./testing/")  # Need to comment if Loesstest_read
    Arrangetest_read()
    cal_enet_read()
    rlnormtest()
    Arrangetest_rl()
    cal_enet_rl()
    Cal_Cor() 
