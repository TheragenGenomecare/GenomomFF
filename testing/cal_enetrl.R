#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

#args <- read.table(args[1], header=FALSE)

#N = args$V1
N = 3881

library(glmnet)
library(Matrix)
library(MASS)
library(methods)
##################################################################################################################
temptrainparasrl = args[1]
temptrain_srl_y = args[2]
temptrain_srl_rf = args[3]
enetsrl = args[4]


print("#########2.gmlnet parameter")

#beta = read.csv("temptrainparasrl1000.csv")
beta = read.csv(temptrainparasrl)

inter = beta$X1[1]
beta <- beta$X1[2:N]
beta[is.na(beta)] <- 0
#names(beta) = bininfo$binName
names(inter) = "Intercept"

#y = read.csv("temptrain_srl_y_117.csv", header=F)
y = read.csv(temptrain_srl_y, header=F)

#rf = read.csv("temptrain_srl_rf_117.csv", header=F)
rf = read.csv(temptrain_srl_rf, header=F)

rf[is.na(rf)] <- 0
x=as.matrix(rf)
y<-as.matrix(y)
###### 3.Matrix #############

print("#########3.Matrix")
for (i in 1:length(y)){
    enet = x[i,] %*% beta+inter
  
    if(i==1){
       final_enet <- c(enet)
    }else{
        final_enet <- c(final_enet, enet)
   }
}
result <- data.frame(final_enet, y)
write.csv(result, file=enetsrl)
