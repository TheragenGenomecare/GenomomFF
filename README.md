# Background
The accurate measure of fetal fraction is important to assure the results of noninvasive prenatal testing. However, measuring fetal fraction could require a huge amount of data and additional costs. Therefore, this study proposes an alternative method of measuring fetal fraction under a limited sample size and low sequencing reads. The adaptive machine learning algorithms customized to each laboratory’s environment were used to measure fetal fraction. The pregnant women with female fetuses were tested to exclude the bias caused by training data of the women carrying male fetuses. The accuracy of fetal DNA fraction prediction was enhanced by increasing the training sample size. When trained with 1,000 samples (males) and tested with 45 samples (females), the optimal bin sizes using the read count and read size features were 300 kb and 800 kb, respectively. Comparing the new 300 kb bin to the 50 kb bin used by SeqFF at 4,000–5,000 training samples, the correlation is approximately 3-5% higher in the 300 kb bin. We have proposed an effective and tailored method to measure fetal fraction available in individual laboratories at limited sample collecting conditions and relatively low-coverage sequencing data.

 <br> `for more search our paper`
# `User Manual`
## Required Files & Folders
##### `The bin info file inside RC and RL file ` as like rc_bin*...  and rl_bininfo*... both  without header

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
 
### " R "
  - doParallel
  - glmnet
  - Matrix
  - MASS
  - methods
  ```bash
install.packages(c('Matrix', 'glmnet', 'MASS', 'foreach', 'doParallel', 'MASS'))
```
  
##### `not installed Python library can be installed by pip install <name> `
##### `not installed R Packages can be installed by install.packages("name")`

#### If any error rise check Files specified Format , installed Packages and Path for Python and R in your System



# Training the Model
### Step 1:
keep all sam File inside sam Folder `TheragenGenomecare/sam/`
Run python code `python bam_rl_read.py` Converting sam file to Read Count rc and  Read Length rl Format. This may take long time according to input size
``` We Focus mainly after this step ```

### Step 2:
Check for Precautions and Requirements . If any Error rises regarding packages then install the required packages

### Step 3 : Run Training Code 
`python GenomomFF_training.py` in same location where GenomomFF_training.py
###### This may take few minute according to your data size <br>
For 1000 sets of data it took around 4 minute in our system 
when training run success fully check parameter csv file inside training Folder

# `Testing the Data`
### Step 4: Check the bininfo files, format and location inside testing Folder
#####  Run testing Code `python GenomomFF_testing.py` 

`` You can See Correlation output and also Correlation csv file saved inside testing folder with correlation value at last ``
#### This program run both on Linux and Windows and we Recommend Windows , Python 3.7 and R 3.6 
### `Any Kinds of Questions ,  Bugs , Suggestions or Eroor are heartly welcome. Thank You`
#### Sunshin Kim (sunshinkim3@gmail.com)
#### Adh Krish (krishdb38@gmail.com)
