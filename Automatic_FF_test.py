#GenomomFF_
import pandas as pd
import numpy as np
import os
import subprocess
import time
import os
import sys 
import shutil #To copy parameter File from test to testing Folder
#from shutil import copyfile
 #

# Declaring Global Variables
#Variable Related to RGC
rgc_bin_info = None #User Input RGC Bin File
ffyrgc = None       # FFyrgc + ... Out put By Loesstrain() Function
trgc   = None       #trgc +.... is  also Output By Loesstrain() Function
temptrain_rgc = None # Output by Arrangetrain() 
temptrain_rgc_y=None #output By Enet() Function Arrangetrain()
temptrain_rgc_rf=None #Output By Enet() Function
temp_train_par_rgc =  "temptrain_par_rgc1000.csv"#Output By GLmnet for Training Purpose
# Global Variable for SRL
srl_bin_info = None #User Input SRL Bin File 
ffysrl = None       # FFyrgc + ... Out put By Loesstrain() Function
tsrl   = None       #trgc +.... is  also Output By Loesstrain() Function
temptrain_srl = None # Output by Arrangetrain() 
temptrain_srl_y=None #output By Enet() Function
temptrain_srl_rf=None #Output By Enet() Function
temp_train_par_srl ="temptrain_par_srl1000.csv" #Output By GLmnet for Training Purpose

def read_bin():

    global srl_bin_info,rgc_bin_info   # info File 
    global ffyrgc,trgc    #RGC R file Output
    global ffysrl,tsrl
    ###############################
    global temptrain_rgc, temptrain_srl
    #Arrange train
    global temptrain_srl_rf, temptrain_srl_y
    global temptrain_rgc_rf, temptrain_rgc_y
    #Parameter Value
    global temp_train_par_rgc , temp_train_par_srl
    
    print("Welcome To FF Analysis 1.0 Version\nTEST")
    #print( "Put your RGC files and rgc_bininfo file in RGC FOLDER")
    #print("Put Your SRL FILes and SRL bin info in SRL FOLDER")
    files = os.listdir("./test/RGC")
    for file in files:
        if file[:10]=="rgcbininfo":
            rgc_bin_info = file
            ffyrgc = "ffyrgc_"+file[11:]
            trgc   = "trgc_"+ file[11:]
            temptrain_rgc = "temptrain_rgc_"+file[11:]          
            temptrain_rgc_rf = "temptrain_rgc_rf"+file[11:]
            temptrain_rgc_y = "temptrain_rgc_y"+file[11:]
            
            #temp_train_par_rgc = "temptrain_par_rgc"+file[11:] 
    if rgc_bin_info == None:#if bin info file not Found No need to run Further
        print("RGC Bininfo file Not found")
        sys.exit(1)
    #for SRL 
    files = os.listdir("./test/SRL")
    for file in files:
        if file[:10] == "srlbininfo":
            srl_bin_info = file
            ffysrl= "ffysrl_"+file[11:]
            tsrl = "tsrl_" + file[11:]
            temptrain_srl = "temptrain_srl_"+file[11:]
            temptrain_srl_rf = "temptrain_srl_rf_"+file[11:]
            temptrain_srl_y = "temptrain_srl_y_"+file[11:]
            
            #temp_train_par_srl = "temptrain_par_srl"+file[11:] #We added Manually
    if srl_bin_info == None:#if bin info file not Found No need to run Further 
        print("SRL Bininfo file Not found")
        sys.exit(1)
        
    print("we found following RGC and SRL bininfo files")
    print("RGC info file is \t",rgc_bin_info)
    print("SRL info file is \t",srl_bin_info)
    return rgc_bin_info , srl_bin_info,ffyrgc ,trgc ,ffysrl ,\
         tsrl,temptrain_rgc,temptrain_rgc_rf,temptrain_rgc_y,temptrain_srl,temptrain_srl_rf,\
             temptrain_srl_y
##First step is receive bininfo file and create 
  

def losetrain_SRL_R():
    global srl_bin_info,ffysrl , tsrl
    os.chdir("./test/SRL") #When Working with RGC FOlder Path Must Be changed
    cmd = ['Rscript',"srlnormtrain.R",srl_bin_info , ffysrl , tsrl]
    #print(os.getcwd())
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("SRLNORMtrain.R Ran SuccessFully")
        print(out.stdout)
        
def Arrangetrain_srl_py():
    #import os
    #os.chdir("./test/SRL/")
    global tsrl , ffysrl
    global temptrain_srl
    global temptrain_srl_rf,temptrain_srl_y
    #All X Variables
    x = pd.read_csv(tsrl)
    x= x.iloc[:,1:]
    x.to_csv(temptrain_srl_rf,index = None ,header = False)
    
    #Y variable is Single
    y = pd.read_csv(ffysrl,usecols=[1])
    y.to_csv(temptrain_srl_y,index = None ,header = False)
    #df_y.to_csv("test")
    df_merge = pd.concat([y,x],axis =1)
    df_merge.to_csv(temptrain_srl)
    
def Loesstrain_srl_pytho():
    global srl_bin_info,ffysrl , tsrl
    os.chdir("./test/SRL")
    
    df =pd.DataFrame()
    infolist = pd.read_csv(srl_bin_info,header = None)
    y = infolist.iloc[:,1]
    y = pd.DataFrame(y/100) #in Percent
    y.to_csv(ffysrl)
    infolist = infolist.iloc[:,0]

    for srl_file in infolist:
        bininfo = pd.read_csv(srl_file)
        bininfo = bininfo.iloc[:,[1,3]]
        print("Readed",srl_file)
        autosomebinsonly = (bininfo.CHR!="chrX")&(bininfo.CHR!="chrY")&(bininfo.CHR!="chr13")&(bininfo.CHR!="chr18")&(bininfo.CHR!="chr21")
    
        sum_rrl_autosomebinsl = bininfo.rrl[autosomebinsonly].sum()
    
        #remove = (bininfo.CHR=="chrX")|(bininfo.CHR=="chrY")|(bininfo.CHR=="chr13")|(bininfo.CHR=="chr18")|(bininfo.CHR=="chr21")
        #instead remove we used autosome bin only both are same
        
        bininfo["allscaledtemp"] = bininfo.rrl/sum_rrl_autosomebinsl
        bininfo["bincounts"]= bininfo.allscaledtemp[autosomebinsonly]/(bininfo.allscaledtemp.sum())*len(bininfo["allscaledtemp"])

        #Since We apply to autosome bins Only so NA value must be replaced with 0
        bininfo =bininfo.fillna(0) #Fill NA = 0
        bin_counts = pd.DataFrame(bininfo.bincounts).T #T is needed to make in row
        df =df.append(bin_counts,ignore_index=True)  #Change if some thing Error rises
    df.to_csv(tsrl)
    #y.to_csv()

def Enet_srl(): #receive temptrain file from arange_train()
    global temptrain_srl,temptrain_srl_y , temptrain_srl_rf,temp_train_par_srl
    #df = pd.read_csv(temptrain_srl,header = None,)
    #(df.iloc[:,0]).to_csv("temptrainy.csv",index = None ,header = False )
    #Write First Column to temptrainy.csv file
    #(df.iloc[:,1:]).to_csv("temptrainrf.csv" ,index = None , header = False) 
    #write a whole file from col 1 to end 
    #temmp_train_y and temptrain_rf already done in Previous Loesstrain_srl_python() Function so Here No Need to Repeet the same function
    
    cmd = ['Rscript', 'glmnet.R',temptrain_srl_y ,temptrain_srl_rf,temp_train_par_srl ]   
    out = subprocess.Popen(cmd , stdout=subprocess.PIPE , stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    if stderr:
            sys.stderr.write(stderr)
            sys.exit(1)
    else:
        print("glmnet.R Ran Successfully")
    #BIN = 800000
    shutil.copy(temp_train_par_srl ,"../")
    
################################################################################################
#####################RGC FILE###################################################################

#print(os.getcwd())
#If Below Code raise Error then change to proper Working directory i.e for same Directory

def Loess_gc_train_rgc():
    global rgc_bin_info,ffyrgc , trgc
    print(rgc_bin_info,ffyrgc,trgc )
    os.chdir("../RGC") #While Running All Code
    #os.chdir("./test/RGC/") #While Running RGC Only
    cmd = ['Rscript','loessgctrain.R',rgc_bin_info ,ffyrgc,trgc ] #Parameter Must be passed bininfo file, Y and X
    
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("SRLNORMtrain.R Ran SuccessFully")
        print(out.stdout)
    
def Arrangetrain_rgc_old():
    global ffyrgc , trgc, temptrain_rgc , temptrain_rgc_rf , temptrain_rgc_y
    #os.chdir("./test/RGC/")
    #a =(os.getcwd())
    #print(str(a))
    sp = {}
    ip = ffyrgc
    input = open(ip,'r')
    check = 0
    for line in input:
        arr = str.split(line,',')
        if check > 0:
            key = check
            if key not in sp:
                sp[key] = []
            sp[key].append(arr[1][:-1])
        check += 1

    ip = trgc
    input = open(ip,'r')
    check = 0
    for line in input:
    #pdb.set_trace()
        arr = str.split(line,',')
        if check > 0:
            key = check
            for k in range(1, len(arr)):
                if key not in sp:
                    sp[key] = []
            if k == len(arr)-1:
                sp[key].append(arr[k][:-1])
            else:
                sp[key].append(arr[k])
        check += 1
        
    out = temptrain_rgc
    output = open(out,'w')
    for x in range(1, len(sp.keys())+1):
        output.write(str(sp[x][0])+',')
        #pdb.set_trace()
        for y in range(1, len(sp[x])):
            #pdb.set_trace()
            if y == len(sp[x])-1:
                output.write(sp[x][y]+'\n')
            else:
                output.write(sp[x][y]+',')
    output.close()        
def Arrangetrain_rgc_new():
    #os.chdir("./test/RGC/")
    #a =(os.getcwd())
    #print(str(a))
    global ffyrgc , trgc, temptrain_rgc , temptrain_rgc_rf , temptrain_rgc_y
    #print(os.getcwd())
    #print(ffyrgc , trgc, temptrain_rgc , temptrain_rgc_rf , temptrain_rgc_y)
    ##################################################cd .
    df_y = pd.read_csv(ffyrgc,usecols=[1])
    df_y = df_y.rename(columns=df_y.iloc[0])
    df_y = df_y.iloc[1:,:]
    df_y.to_csv(temptrain_rgc_y,index = None)

    #Variable Y
    df_x = pd.read_csv(trgc) #Read CSV
    df_x= df_x.iloc[:,1:] #Remove First Col 
    df_x = df_x.rename(columns=df_x.iloc[0]) #Rename the First Column
    df_x = df_x.iloc[1:,:] #Since First Row is make as Col header so remove First row
    df_x.to_csv(temptrain_rgc_rf,index = None ) #Save the File
    #The below File is not used 
    pd.concat([df_y , df_x],axis =1).to_csv("temptrain_rgc.csv",index =None)
    
def Enet_rgc():
    global temptrain_rgc_rf , temptrain_rgc_y,temp_train_par_rgc
    #In This Enet We dont Need to find out temp train y and x because We Already Find Out this in Arrangetrain_rgc()\
    #We Only Run R Script here
    cmd = ["Rscript",'glmnet.R' , temptrain_rgc_y,temptrain_rgc_rf,temp_train_par_rgc]
    out = subprocess.run(cmd,shell=True,capture_output =True, text=True)
    if out.returncode !=0:
        print("Error rises")
        print(out.stderr)
        print(out.returncode)
    else:
        print("GLMNET.R Ran SuccessFully")
        print(out.stdout)
        
    shutil.copy(temp_train_par_rgc ,"../")


if __name__ == "__main__":
    #print("run Code")
    read_bin() #This Function always be open; Variable declaration is inside there
    
    #print(os.getcwd())
    #os.chdir("./test/SRL/") #if You want to crun step by step then
    losetrain_SRL_R()
    #Loesstrain_srl_pytho()
    Arrangetrain_srl_py()
    Enet_srl()
    
    #here also need to check WD Directory while running one by One
    #os.chdir("./test/RGC")
    #Loess_gc_train_rgc() #if Error raised Working Directory must be check
    #Arrangetrain_rgc_new()
    #Arrangetrain_rgc_old()
    #Enet_rgc()
