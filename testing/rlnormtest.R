#!/usr/bin/R
args = commandArgs(trailingOnly=TRUE)

library(Matrix)
srl_file = args[1]
ffysr_ = args[2]
tsrl_ = args[3]

N = 3881

rrl_list = read.table(srl_file,sep=",")
y <- rrl_list$V2
rrl_list <- rrl_list$V1

for(i in seq_along(rrl_list)) {

  name = paste(rrl_list[i],sep="")

  #bininfo is change to bin autosomebinsonly change to auto_bin
  
  bin = read.csv(name)

  auto_bin = bin$CHR!="chrX" & bin$CHR!="chrY" & bin$CHR!="chr13" & bin$CHR!="chr18" & bin$CHR!="chr21"
  alluseablebins = bin$BIN

  autoscaledtemp  <- bin$RRL[auto_bin]/sum(bin$RRL[auto_bin], na.rm=T)
  allscaledtemp  <- bin$RRL[alluseablebins]/sum(bin$RRL[auto_bin], na.rm=T)

  remove = bin$CHR=="chrX" | bin$CHR=="chrY" | bin$CHR=="chr13" | bin$CHR=="chr18" | bin$CHR=="chr21"
  names(remove) = bin$BIN

  normalizedbincount <- allscaledtemp 

  bincounts=rep(1,N-1)
  names(bincounts) = bin$BIN
  bincounts[alluseablebins] <- (normalizedbincount/sum(normalizedbincount, na.rm=T)) * length(normalizedbincount)
  bincounts[is.na(bincounts)] <- 0
  df <- data.frame(bin$CHR, bincounts)
  bincounts[remove] <- 0

  if(i==1){
    all_mat=matrix(bincounts,1,N-1)
  }else{
    mat=matrix(bincounts,1,N-1)
    all_mat <- rbind(all_mat,mat)
  }
  ID = strsplit(as.character(rrl_list[i]), "_")
  cat("\t",ID[[1]][1])
}
y <- y*0.01
ymat <- as.matrix(y)
tmat <- as.matrix(all_mat)
write.csv(ymat, file = ffysr_) #Except Row name
write.csv(tmat, file = tsrl_) #Except First Col row name
print("RLNORMTRAIN.R RAN Successfully")
