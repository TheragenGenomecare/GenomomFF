#!/usr/bin/R
args = commandArgs(trailingOnly=TRUE)

#args <- read.table(args[1], header=FALSE)

#N = args$V1
library(Matrix)
srl_file = args[1]
ffysr_ = args[2]
tsrl_ = args[3]
#srl_file = "srlbininfo" Automatically Passed by Progtram
N = 3881

infolist = read.table(srl_file,sep=",")


y <- infolist$V2
infolist <- infolist$V1

for(i in seq_along(infolist)) {
  #print(infolist[i])
  #name = paste("~/seqFF/bininfo1/",infolist[i],sep="")
  name = paste(infolist[i],sep="")

  bininfo = read.csv(name)

  autosomebinsonly = bininfo$CHR!="chrX" & bininfo$CHR!="chrY" & bininfo$CHR!="chr13" & bininfo$CHR!="chr18" & bininfo$CHR!="chr21"
  alluseablebins = bininfo$binName

  autoscaledtemp  <- bininfo$rrl[autosomebinsonly]/sum(bininfo$rrl[autosomebinsonly], na.rm=T)
  allscaledtemp  <- bininfo$rrl[alluseablebins]/sum(bininfo$rrl[autosomebinsonly], na.rm=T)

  remove = bininfo$CHR=="chrX" | bininfo$CHR=="chrY" | bininfo$CHR=="chr13" | bininfo$CHR=="chr18" | bininfo$CHR=="chr21"
  names(remove) = bininfo$binName

  normalizedbincount <- allscaledtemp 

  bincounts=rep(1,N-1)
  names(bincounts) = bininfo$binName
  bincounts[alluseablebins] <- (normalizedbincount/sum(normalizedbincount, na.rm=T)) * length(normalizedbincount)
  bincounts[is.na(bincounts)] <- 0
  df <- data.frame(bininfo$CHR, bincounts)
  bincounts[remove] <- 0

  if(i==1){
    all_mat=matrix(bincounts,1,N-1)
  }else{
    mat=matrix(bincounts,1,N-1)
    all_mat <- rbind(all_mat,mat)
  }
  ID = strsplit(as.character(infolist[i]), "_")
  cat("\t",ID[[1]][1])
}
y <- y*0.01
ymat <- as.matrix(y)
tmat <- as.matrix(all_mat)
write.csv(ymat, file = ffysr_) #Except Row name
write.csv(tmat, file = tsrl_) #Except First Col row name
print("RLNORMTRAIN.R RAN Successfully")
