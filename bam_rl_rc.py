#!usr/bin/python3
import sys,os

sam_files =[]
ls =  os.listdir("./samfile/") #keep ALl Sam Files here
for file in ls:
    if file[-3:]=="sam":
        sam_files.append(file)
        print(file)
print("Total sam Files= ",len(sam_files))

#Define a function to convert sam_file to sam_rgc.csv Format
def sam_2_rc():
    count = 1
    #sam_file_name ,  Bin_ =300000, fkbin_ = 50000
    global sam_files
    Bin =300000
    fkbin = 50000
    print("converting Sam file to RC")
     # List of sam Files
    
    for sam_file_name in sam_files:
        list_input = open("./samfile/"+sam_file_name,'r') #Read SAM File
        list_text = list_input.readlines()  #Read Line by Line and store in list format values
        output = open("./samfile/"+sam_file_name+'.rc', 'w')  #Save file
        rd = a1 = c1 = g1 = t1 =0
        #Bin = Bin_ #30K
        #fkbin = fkbin_ #gap in read
        mx = [4985*fkbin/Bin, 4863*fkbin/Bin, 3960*fkbin/Bin, 3823*fkbin/Bin, 3618*fkbin/Bin, 3422*fkbin/Bin, 3182*fkbin/Bin,\
            2927*fkbin/Bin, 2824*fkbin/Bin,2710*fkbin/Bin, 2700*fkbin/Bin, 2677*fkbin/Bin, 2303*fkbin/Bin, 2146*fkbin/Bin,\
            2050*fkbin/Bin, 1807*fkbin/Bin, 1623*fkbin/Bin, 1561*fkbin/Bin,1182*fkbin/Bin, 1260*fkbin/Bin, 962*fkbin/Bin, \
            1026*fkbin/Bin, 3105*fkbin/Bin, 1187*fkbin/Bin]

        sp = {}
        for x in range(22):
            for y in range(int(mx[x])+1):
                key = 'chr'+str(x+1)+"_"+str(y)
                if key not in sp:
                    sp[key] = []  #Blank Container
                sp[key].append(key)
                sp[key].append(rd)
                sp[key].append(a1)
                sp[key].append(c1)
                sp[key].append(g1)
                sp[key].append(t1)

        for y in range(int(mx[22]+1)):
            key = "chrX"+"_"+str(y)
            if key not in sp:
                sp[key] = [] #Blank Container to store New Value
            sp[key].append(key)
            sp[key].append(rd)
            sp[key].append(a1)
            sp[key].append(c1)
            sp[key].append(g1)
            sp[key].append(t1)

        for y in range(int(mx[23]+1)):
            key = "chrY"+"_"+str(y)
            if not key in sp:
                sp[key] = [] #Blank Container to store new Value
            sp[key].append(key)
            sp[key].append(rd)
            sp[key].append(a1)
            sp[key].append(c1)
            sp[key].append(g1)
            sp[key].append(t1)

        for line in list_text:
            arr = line.split()
            try:
                temp = int(arr[3])/Bin   #we define bin is 300K
                temp = int(temp)
                key = arr[2]+'_'+str(temp)   #arr[2] is chromosome name like chr1 
                if key == sp[key][0]:
                    sp[key][1] += 1
                    for k in range(len(arr[9])):
                        if arr[9][k] == 'A':
                            sp[key][2] += 1
                        elif arr[9][k] == 'C':
                            sp[key][3] += 1
                        elif arr[9][k] == 'G':
                            sp[key][4] += 1
                        elif arr[9][k] == 'T':
                            sp[key][5] += 1

            except:
                pass 

        output.write('"BIN"'+','+'"CHR"'+','+'END'+','+'"COUNT"'+','+'"GC"'+'\n')
        for x in range(1, 23):
            for y in range(int(mx[x-1])+1):
                key = "chr"+str(x)+'_'+str(y)
                count = sp[key][1]
                a1 = sp[key][2]
                c1 = sp[key][3]
                g1 = sp[key][4]
                t1 = sp[key][5]
                if a1 == 0 and c1 == 0 and g1 == 0 and t1 == 0:
                    output.write("chr"+str(x)+'_'+str(y)+','+"chr"+str(x)+','+str(Bin*(y+1))+','+str(0)+','+str(0)+'\n')
                else:
                    output.write("chr"+str(x)+'_'+str(y)+','+"chr"+str(x)+','+str(Bin*(y+1))+','+str(count)+','+str(float(c1+g1)/float(a1+c1+g1+t1))+'\n')

        for y in range(int(mx[22]+1)):
            key = "chrX"+'_'+str(y)
            count = sp[key][1]
            a1 = sp[key][2]
            c1 = sp[key][3]
            g1 = sp[key][4]
            t1 = sp[key][5]
            if a1 == 0 and c1 == 0 and g1 == 0 and t1 == 0:
                output.write("chrX"+'_'+str(y)+','+"chrX"+','+str(Bin*(y+1))+','+str(0)+','+str(0)+'\n')
            else:
                output.write("chrX"+'_'+str(y)+','+"chrX"+','+str(Bin*(y+1))+','+str(count)+','+str(float(c1+g1)/float(a1+c1+g1+t1))+'\n')

        for y in range(int(mx[23]+1)):
            key = "chrY"+'_'+str(y)
            count = sp[key][1]
            a1 = sp[key][2]
            c1 = sp[key][3]
            g1 = sp[key][4]
            t1 = sp[key][5]
            if a1 == 0 and c1 == 0 and g1 == 0 and t1 == 0:
                output.write("chrY"+'_'+str(y)+','+"chrY"+','+str(Bin*(y+1))+','+str(0)+','+str(0)+'\n')
            else:
                output.write("chrY"+'_'+str(y)+','+"chrY"+','+str(Bin*(y+1))+','+str(count)+','+str(float(c1+g1)/float(a1+c1+g1+t1))+'\n')
            
        output.close()
        count +=1
    #print("Sam to SRG Completed=",count)
    print("All sam File Converted to RC")


def sam_to_rl():
    #sam_file_name,output_folder = "./test/SRL800K/" , Bin = 800000,fkbin = 50000
    global sam_files
    print("Converting SAM to RL")
    count =1
    #var1 = sam_file_name
    #out = sam_file_name[9:] #sam_file/ == 8 Character
    Bin = 800000
    fkbin = 50000
    
    #open the File in loop
    for sam in sam_files:
        list_input = open("./samfile/"+sam,'r')
        list_text = list_input.readlines()
        output = open("./samfile/"+sam+'.rl', 'w')
        rd = srd = 0
    

        mx = [4985*fkbin/Bin, 4863*fkbin/Bin, 3960*fkbin/Bin, 3823*fkbin/Bin, 3618*fkbin/Bin, 3422*fkbin/Bin, 3182*fkbin/Bin, 2927*fkbin/Bin, 2824*fkbin/Bin, 2710*fkbin/Bin, 2700*fkbin/Bin, 2677*fkbin/Bin, 2303*fkbin/Bin, 2146*fkbin/Bin, 2050*fkbin/Bin, 1807*fkbin/Bin, 1623*fkbin/Bin, 1561*fkbin/Bin, 1182*fkbin/Bin, 1260*fkbin/Bin, 962*fkbin/Bin, 1026*fkbin/Bin, 3105*fkbin/Bin, 1187*fkbin/Bin]

        sp = {}
        for x in range(22):
        
            for y in range(int(mx[x])+1): #Converted to Integer
                key = 'chr'+str(x+1)+"_"+str(y)
                if key not in sp:
                    sp[key] = []
                sp[key].append(key)
                sp[key].append(rd)
                sp[key].append(srd)

        for y in range(int(mx[22])+1):
            key = "chrX"+"_"+str(y)
            if key not in sp:
                sp[key] = []
            sp[key].append(key)
            sp[key].append(rd)
            sp[key].append(srd)

        for y in range(int(mx[23])+1):
            key = "chrY"+"_"+str(y)
            if key not in sp:
                sp[key] = []
            sp[key].append(key)
            sp[key].append(rd)
            sp[key].append(srd)

        for line in list_text:
            arr = line.split()
            try:
                temp = int(arr[3])/Bin
                temp = int(temp)
                key = arr[2]+'_'+str(temp)
                if key == sp[key][0]:
                    sp[key][1] += 1
                    if len(arr[9]) < 150:
                        sp[key][2] += 1

            except:
                pass 

        output.write('"BIN"'+','+'"CHR"'+','+'"END"'+','+'"RRL"'+'\n')
        for x in range(1, 23):
            for y in range(int(mx[x-1])+1):
                key = "chr"+str(x)+'_'+str(y)
                count = sp[key][1]
                srcount = sp[key][2]
                if count == 0 and srcount == 0:
                    output.write("chr"+str(x)+'_'+str(y)+','+"chr"+str(x)+','+str(Bin*(y+1))+','+str(0)+'\n')
                else:
                    output.write("chr"+str(x)+'_'+str(y)+','+"chr"+str(x)+','+str(Bin*(y+1))+','+str(float(srcount)/float(count))+'\n')

        for y in range(int(mx[22])+1):
            key = "chrX"+'_'+str(y)
            count = sp[key][1]
            srcount = sp[key][2]
            if count == 0 and srcount == 0:
                output.write("chrX"+'_'+str(y)+','+"chrX"+','+str(Bin*(y+1))+','+str(0)+'\n')
            else:
                output.write("chrX"+'_'+str(y)+','+"chrX"+','+str(Bin*(y+1))+','+str(float(srcount)/float(count))+'\n')

        for y in range(int(mx[23])+1):
            key = "chrY"+'_'+str(y)
            count = sp[key][1]
            srcount = sp[key][2]
            if count == 0 and srcount == 0:
                output.write("chrY"+'_'+str(y)+','+"chrY"+','+str(Bin*(y+1))+','+str(0)+'\n')
            else:
                output.write("chrY"+'_'+str(y)+','+"chrY"+','+str(Bin*(y+1))+','+str(float(srcount)/float(count))+'\n')
        count +=1
        output.close()

if __name__ == "__main__":
    sam_2_rc()
    sam_to_rl()