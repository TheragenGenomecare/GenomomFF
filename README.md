# Background
The accurate measure of fetal fraction is important to assure the results of noninvasive prenatal testing. However, measuring fetal fraction could require a huge amount of data and additional costs. Therefore, this study proposes an alternative method of measuring fetal fraction under a limited sample size and low sequencing reads. The adaptive machine learning algorithms customized to each laboratory’s environment were used to measure fetal fraction. The pregnant women with female fetuses were tested to exclude the bias caused by training data of the women carrying male fetuses. The accuracy of fetal DNA fraction prediction was enhanced by increasing the training sample size. When trained with 1,000 samples (males) and tested with 45 samples (females), the optimal bin sizes using the read count and read size features were 300 kb and 800 kb, respectively. Comparing the new 300 kb bin to the 50 kb bin used by SeqFF at 4,000–5,000 training samples, the correlation is approximately 3-5% higher in the 300 kb bin. We have proposed an effective and tailored method to measure fetal fraction available in individual laboratories at limited sample collecting conditions and relatively low-coverage sequencing data.

 <br> `for more search our paper`
# `User Manual`
## Required Files & Folders
##### `The bin info file inside RC and RL file ` are like rc_bin*...  and rl_bininfo*... both  without header

Sample1.Fastq.sam.bam.sort.bam.rmdup.bam.sam.rl,19.05270566
Sample2.Fastq.sam.bam.sort.bam.rmdup.bam.sam.rl,17.65618359

##### Read Count (RC) and Read Length (RL) file must be in .rc and .rl format and header as like <br>
"BIN","CHR","END","COUNT","GC" <br>
chr1_0,chr1,300000,583,0.430783082518<br>
chr1_1,chr1,600000,474,0.444418530072<br>

"BIN","CHR","END","RRL"<br>
chr1_0,chr1,800000,0.255024255024<br>
chr1_1,chr1,1600000,0.262870514821 <br>

### Require dependency
### `Python greater than 3`
 - Pandas 
 - numpy
 - scikit
   
   ```Method to insall python library pip install <library name> e.g. pip install pandas ```
 
### " R "
  - doParallel
  - glmnet
  - Matrix
  - MASS
  - methods
  
  ```install.packages(c('Matrix', 'glmnet', 'MASS', 'foreach', 'doParallel', 'MASS'))```

#### If any error rise check Files specified Format , installed Packages and Path for Python and R in your System

# Preparing data for Training & Testing
### Check File Format , Location , bin info file name and header (Column Name) 
Keep all sam File inside sam Folder `TheragenGenomecare/sam/` <br>
Run python code `python bam_rl_read.py` <br> 
Converting sam file to Read Count rc and  Read Length rl Format. This may take long time according to input size
### After rc and rl file ready keep all rc and rl files in training and testing Folders with corresponding bininfo files

## ``` Training the Model ```
`python GenomomFF_training.py`  on terminal where GenomomFF_training.py is located

###### This may take few minute according to your data size <br>
For 1000 sets of data it took around 4 minute in our system 
After running GenomomFF_training successfully , this will create a rc and rl parameter  file inside training Folder which is used for testing the model

## `Testing the Data`
### Check the bininfo files, format and location inside testing Folder
#####  Run testing Code 
```python GenomomFF_testing.py``` 

`` You can See Correlation output and also Correlation csv file saved inside testing folder with correlation value at last ``
#### This program run both on Linux and Windows and we Recommend Windows , Python 3.7 and R 3.6 
### `Any Kinds of Questions ,  Bugs , Suggestions or Error are heartly welcome. Thank You`
#### Sunshin Kim (sunshinkim3@gmail.com)
#### Adh Krish (krishdb38@gmail.com)
