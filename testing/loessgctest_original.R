#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

#args <- read.table(args[1], header=FALSE)

#N = args$V1
N = 10333
rgcb_info = args[1]
ffyrgc_out= args[2]
trgc_out= args[3]

print(rgcb_info)

infolist = read.table(rgcb_info,sep = ",")

y <- infolist$V2
infolist <- infolist$V1

for(i in seq_along(infolist)) {
  #print(infolist[i])
  #name = paste("~/seqFF/bininfo1/",infolist[i],sep="")
  name = paste(infolist[i],sep=",") #This is Comma seprated File sep="" if ts
  bininfo = read.csv(name)

  ############ create bincounts infomation 
#  autosomebinsonly = bininfo$CHR!="chrX" & bininfo$CHR!="chrY"
#  alluseablebins = bininfo$BinFilterFlag==1 | bininfo$BinFilterFlag==0
  autosomebinsonly = bininfo$CHR!="chrX" & bininfo$CHR!="chrY" & bininfo$CHR!="chr13" & bininfo$CHR!="chr18" & bininfo$CHR!="chr21"
  alluseablebins = bininfo$binName

  autoscaledtemp  <- bininfo$counts[autosomebinsonly]/sum(bininfo$counts[autosomebinsonly], na.rm=T)
  allscaledtemp  <- bininfo$counts[alluseablebins]/sum(bininfo$counts[autosomebinsonly], na.rm=T)

  remove = bininfo$CHR=="chrX" | bininfo$CHR=="chrY" | bininfo$CHR=="chr13" | bininfo$CHR=="chr18" | bininfo$CHR=="chr21"
  names(remove) = bininfo$binName

  # additive loess correction
  meancountpergc <- tapply(
    autoscaledtemp,round(bininfo$nGC[autosomebinsonly], digits=3), function(x) mean(x, na.rm=T))
  ## prediction 
  loess.fitted  <- predict( loess(meancountpergc ~ as.numeric(names(meancountpergc))), round(bininfo$nGC[alluseablebins], digits=3)) 
  normalizedbincount <- allscaledtemp  + ( mean(autoscaledtemp, na.rm=T) - loess.fitted )  

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
  print(ID[[1]][1])
}
y <- y*0.01
ymat <- as.matrix(y)
tmat <- as.matrix(all_mat)
write.csv(ymat, file = ffyrgc_out)
write.csv(tmat, file = trgc_out) 
