# Author:Sunshin Kim (sunshinkim3@gmail.com)
# Krishna(krishdb38@gmail.com)

import pandas as pd
import numpy as np
#from shutil import copyfile
import shutil
import os
import subprocess
import time
import sys
print("Welcome To FF Analysis 1.0 Version\nTEST")
print("Prototype Developed By Sunshin Kim (sunshinkim3@gmail.com) ")
print("Code updated by Adh Krish krishdb38@gmail.com \n")

# To copy parameter File from test to testing Folder
# In DNA sequencing, a rc is an inferred sequence of base pairs
# (or base pair probabilities) corresponding to all or part of a single DNA fragment
rc_bin_info = None
rl_bin_info = None  # User Input rc Bin File
ffy_rc = None
t_rc =None
ffy_rl =None
t_rl = None  # Dependent and Independend Variables
temptrain_rc_y =None
temptrain_rc_rf =None
temptrain_rl_y = None
temptrain_rl_rf = None
# Output By GLmnet for Training Purpose
temp_train_par_rc = "temptrain_par_rc.csv"

# Output By GLmnet for Training Purpose
temp_train_par_rl = "temptrain_par_rl.csv"


def read_bin():
    global rl_bin_info, rc_bin_info, ffy_rc, t_rc, ffy_rl, t_rl
    global temptrain_rl_rf, temptrain_rl_y
    global temptrain_rc_rf, temptrain_rc_y

    files = os.listdir("./training/RC/")
    for file in files:
        if file[:6] == "rc_bin":
            rc_bin_info = file
            ffy_rc = "ffy_rc_"+file[13:]
            t_rc = "t_rc_" + file[13:]
            temptrain_rc_rf = "temptrain_rc_rf"+file[6:]
            temptrain_rc_y = "temptrain_rc_y"+file[6:]
            print("rc info file is \t", rc_bin_info)
    if rc_bin_info == None:
        print("rc Bininfo file Not found")
        sys.exit(1)  # if rc bin info file not Found No need to run Further
    # for  Length
    files = os.listdir("./training/RL/")
    for file in files:
        if file[:6] == "rl_bin":
            rl_bin_info = file
            ffy_rl = "ffy_rl_"+file[6:]
            t_rl = "t_rl_" + file[6:]
            temptrain_rl_rf = "temptrain_rl_rf_"+file[6:]
            temptrain_rl_y = "temptrain_rl_y_"+file[6:]
            print("RL info file is \t", rl_bin_info)
    if rl_bin_info == None:  # if bin info file not Found No need to run Further
        print("RL Bininfo file Not found")
        sys.exit(1)


def Rl_normtrain():
    global rl_bin_info, ffy_rl, t_rl
    os.chdir("./training/RL/")
    df = pd.DataFrame()
    infolist = pd.read_csv(rl_bin_info, header=None)
    y = infolist.iloc[:, 1]
    y = pd.DataFrame(y/100)  # in Percent
    y.to_csv(ffy_rl)
    infolist = infolist.iloc[:, 0]
    for rl_file in infolist:
        bininfo = pd.read_csv(rl_file)
        bininfo = bininfo.iloc[:, [1, 3]]
        
        autosomebins = (bininfo.CHR != "chrX") & (bininfo.CHR != "chrY") & (
            bininfo.CHR != "chr13") & (bininfo.CHR != "chr18") & (bininfo.CHR != "chr21")

        sum_rrl_autosomebinsl = bininfo.RRL[autosomebins].sum()
        #remove = (bininfo.CHR=="chrX")|(bininfo.CHR=="chrY")|(bininfo.CHR=="chr13")|(bininfo.CHR=="chr18")|(bininfo.CHR=="chr21")
        # instead remove we used autosome bin only both are same
        bininfo["allscale"] = bininfo.RRL/sum_rrl_autosomebinsl
        bininfo["bincounts"] = bininfo.allscale[autosomebins] / \
            (bininfo.allscale.sum())*len(bininfo["allscale"])
        # Since We apply to autosome bins Only so NA value must be replaced with 0
        bininfo = bininfo.fillna(0)  # Fill NA = 0
        bin_counts = pd.DataFrame(bininfo.bincounts).T  # T is Transpose Numpy
        # Change if some thing Error rises
        df = df.append(bin_counts, ignore_index=True)
    df.to_csv(t_rl)


def Arrangetrain_rl():
    global t_rl, ffy_rl, temptrain_rl_rf, temptrain_rl_y
    x = pd.read_csv(t_rl)  # All X Variables
    x = x.iloc[:, 1:]
    x.to_csv(temptrain_rl_rf, index=None, header=False)
    y = pd.read_csv(ffy_rl, usecols=[1])  # Col 1 is selected Directly
    y.to_csv(temptrain_rl_y, index=None, header=False)
    print("Arrange_train RL Run Successfully")

def Enet_rl():  # receive temptrain file from arange_train()
    global temptrain_rl_y, temptrain_rl_rf, temp_train_par_rl
    cmd = ['Rscript', 'glmnet.R', temptrain_rl_y,
           temptrain_rl_rf, temp_train_par_rl]
    out = subprocess.run(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    print(out.stderr) if out.stderr else print("Enet R RL Run Success..")
    shutil.copy(temp_train_par_rl, "../")
    print("temptrain par rl file is copied..")


##################### rc FILE###################################################################


def Loess_gc_train_rc():
    os.chdir("../RC/")  # While Running All Code
    global rc_bin_info, ffy_rc, t_rc
    cmd = ['Rscript', 'loessgctrain.R', rc_bin_info, ffy_rc, t_rc]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(out.stderr) if out.stderr else print("Loess_GC_Trained Success")  # if out.returncode !=0


def Arrangetrain_rc():
    global ffy_rc, t_rc, temptrain_rc_y, temptrain_rc_rf
    df_y = pd.read_csv(ffy_rc, usecols=[1])
    df_y = df_y.rename(columns=df_y.iloc[0])
    df_y = df_y.iloc[1:, :]
    df_y.to_csv(temptrain_rc_y, index=None)
    # Variable Y
    df_x = pd.read_csv(t_rc)  # rc CSV
    df_x = df_x.iloc[:, 1:]  # Remove First Col
    df_x = df_x.rename(columns=df_x.iloc[0])  # Rename the First Column
    # Since First Row is make as Col header so remove First row
    df_x = df_x.iloc[1:, :]
    df_x.to_csv(temptrain_rc_rf, index=None)  # Save the File
    print("Arrange train Successful")


def Enet_rc():
    print("Running ENET R \t", end=" ")
    global temptrain_rc_y, temptrain_rc_rf, temp_train_par_rc
    cmd = ["Rscript", 'glmnet.R', temptrain_rc_y,
           temptrain_rc_rf, temp_train_par_rc]
    out = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    print(out.stderr) if out.stderr else print(out.stdout)
    shutil.copy(temp_train_par_rc, "../")
    print("ENET Ran rc Successfully")


if __name__ == "__main__":
    read_bin()  # This Function always be open; Variable declaration is inside there
    Rl_normtrain()
    #os.chdir("./training/RL/")  # if not Rl_normtrain() run
    Arrangetrain_rl()
    Enet_rl()

    #os.chdir("./training/RC/") # Un comment this if You want to run the below Code seprately
    Loess_gc_train_rc()  # if Error raised Working Directory must be check
    Arrangetrain_rc()
    Enet_rc()