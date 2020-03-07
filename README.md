# Background
The accurate measure of fetal fraction is important to assure the results of noninvasive prenatal testing. However, measuring fetal fraction could require a huge amount of data and additional costs. Therefore, this study proposes an alternative method of measuring fetal fraction under a limited sample size and low sequencing reads. The adaptive machine learning algorithms customized to each laboratory’s environment were used to measure fetal fraction. The pregnant women with female fetuses were tested to exclude the bias caused by training data of the women carrying male fetuses. The accuracy of fetal DNA fraction prediction was enhanced by increasing the training sample size. When trained with 1,000 samples (males) and tested with 45 samples (females), the optimal bin sizes using the read count and read size features were 300 kb and 800 kb, respectively. Comparing the new 300 kb bin to the 50 kb bin used by SeqFF at 4,000–5,000 training samples, the correlation is approximately 3-5% higher in the 300 kb bin. We have proposed an effective and tailored method to measure fetal fraction available in individual laboratories at limited sample collecting conditions and relatively low-coverage sequencing data.

 <br> `for more search our paper`
# `User Manual`
## Required Files in the Folders
##### `The bin info files in RC and RL folders` are like both rc_bin*...  and rl_bininfo*... without headers.

Sample1.Fastq.sam.bam.sort.bam.rmdup.bam.sam.rl,19.05270566
Sample2.Fastq.sam.bam.sort.bam.rmdup.bam.sam.rl,17.65618359

##### Read Count (RC) and Read Length (RL) files must be in .rc and .rl formats with headers as the following. <br>
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
   
   ```Method to insall python library pip install <library name> e.g. pip install pandas. ```
 
### " R "
  - doParallel
  - glmnet
  - Matrix
  - MASS
  - methods
  
  ```install.packages(c('Matrix', 'glmnet', 'MASS', 'foreach', 'doParallel', 'MASS'))```

#### If any error rises, please check the specified format of files, the installed Packages, and the Path for Python and R in your System.

# Preparing data for Training & Testing
### Check file formats, locations, bin info file names, and headers. (Column Name) 
Keep all sam files inside the sam folder like e.g. `TheragenGenomecare/sam/`. <br>
Run python code `python bam_rl_read.py`. <br> 
Convert sam files to Read Count (rc) and Read Length (rl) format files. This may take long time according to the input data size.
### After the rc and rl files are ready, please keep all rc and rl files in training and testing Folders with corresponding bininfo files.

## ``` Training the Model ```
`python GenomomFF_training.py` on terminal where GenomomFF_training.py is located.

###### This may take few minute according to your data size. <br>
For 1000 sets of data, it took around 4 minute in our system. 
After running GenomomFF_training successfully, this will create the rc and rl parameter files inside the training folder, which are used for testing the data.

## `Testing the Data`
### Pleae check the bininfo files, formats, and locations inside testing Folder.
#####  Run testing Code 
```python GenomomFF_testing.py``` 

`` You can See a correlation csv file saved inside testing folder with correlation value at last. ``
#### This program run both on Linux and Windows and we Recommend Windows with Python 3.7 and R 3.6. 
### `Any Kinds of Questions, Bugs, Suggestions or Errors are heartly welcome. Thank You`
#### Sunshin Kim (sunshinkim3@gmail.com)
#### Adh Krish (krishdb38@gmail.com)
