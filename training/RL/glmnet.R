#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
library(glmnet)
library(Matrix)
library(MASS)
library(doParallel)
library(methods)
registerDoParallel(40)

#Automatically Receive Files From Python Parameter
##################################################################################################################

temp_train_y = args[1]
temp_train_rf = args[2]
temp_train_par_rl = args[3]

#cat("#########1.bininfo_file check")
y = read.csv(temp_train_y, header=F)
rf = read.csv(temp_train_rf, header=F)
rf[is.na(rf)] <- 0
###### 3.Matrix #############
#cat("#########3.Matrix")
x=as.matrix(rf)
#x = rf
y<-as.matrix(y)
#y<-y*0.01
###### 4.cv.glmnet ###############################################################################################
#cat("#########4.cv.glmnet")

seqFF_para_cv = cv.glmnet(x, y, alpha=.01, grouped = FALSE, nfolds=10, parallel=TRUE)
#par(mar = rep(2, 4))
#plot(seqFF_para_cv)
###### 5.coef/save ###############################################################################################
#cat("#########5.coef()/save")

#seqFF_para_cv_result <-coef(seqFF_para_cv, s=seqFF_para_cv$lambda.min)
seqFF_para_cv_result <-coef(seqFF_para_cv, s="lambda.min")
result <- as.data.frame(as.matrix(seqFF_para_cv_result))
#write.csv(result,file="~/seqFF/test_result.csv")
write.csv(result,file=temp_train_par_rl)