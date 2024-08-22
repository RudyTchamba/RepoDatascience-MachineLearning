#Load library
library(lattice)
library(DMwR2)
library(dplyr)

#Move to your work directory
getwd()
setwd("C:/Users/Huawei/Documents/INFO L3 2023-2024/DataMining/script_R")

#Read the data into the csv file
df<-read.table(file = "crx.data.txt",sep = ",",header = FALSE,
               na.strings = c("?"))

#View your data
View(df)
summary(df)
dim(df)

#Set the colnames en rownames in my data
rownames(df)<-paste("ind",1:dim(df)[1],sep = "@")
colnames(df)<-paste("V",1:dim(df)[2],sep = "")

#View your data again
View(df)
summary(df)
dim(df)

#Check the missing values
missing_m1<-apply(is.na(df), 2, sum)
missing_m1<-data.frame(missing_m1[missing_m1!=0])

#Other method to check missing values
missing_m2<-colSums(is.na(df))
missing_m2<-data.frame(missing_m2[missing_m2!=0])

#Column names of variables with missing values
var_with_na=rownames(missing_m1)

#Identificate row with missing values

# Method 1 : Using dplyr
df_filter=df %>% select(var_with_na)
ind_with_na=rownames(mutate(df_filter,na_count=rowSums(is.na(df_filter))) %>% filter(na_count>0))

#Method 2 : Using basic function of R
count_row=rowSums(is.na(df))
ind_with_na2=names(count_row[count_row!=0])


#Define 2 bloc for one plot.
par(mfrow=c(1,2))
#histogram of variable V2 with density 
hist(df$V2,xlab = "value of V2", main = "Histogram of V2 with density",probability = TRUE)

#histogram of variable V2 with frequency 
hist(df$V2,xlab = "value of V2", main = "Histogram of V2 with density",probability = TRUE)

#Define 1 bloc for one plot.
par(mfrow=c(1,1))
#histogram of variable V2 with density 
hist(df$V2,xlab = "value of V2", main = "Histogram of V2 with density",probability = TRUE)

#Plot of V2
plot(df$V2, ylab = "Value of V2")

#Boxplot of V2
boxplot(df$V2,  ylab = "Value of V2")

#Bar plot of V1
V1_count=count(df,V1)
barplot(V1_count$n~V1_count$V1, xlab = "V1 value", ylab = "Count")

#Check the outliers for V2
#Plot of V2
plot(df$V2, ylab = "Value of V2", pch=22,col="black")
abline(h = mean(df$V2,na.rm=TRUE),col="red", lty = 2)
abline(h = mean(df$V2,na.rm=TRUE)+sd(df$V2,na.rm = TRUE),col="blue",lty=3)
abline(h=median(df$V2,na.rm=TRUE),col="green",lty=4)

#Identify the outliers
limit_v2=mean(df$V2,na.rm=TRUE)+sd(df$V2,na.rm = TRUE)
df$V2[df$V2>limit_v2 & !is.na(df$V2)]

#For outliers identification you can use the function identier to identify graphically the outliers
outliers_v2=identify(df$V2)


#Check the outliers for V3
#Plot of V2
plot(df$V3, ylab = "Value of V3", pch=22,col="black")
abline(h = mean(df$V3,na.rm=TRUE),col="red", lty = 2)
abline(h = mean(df$V3,na.rm=TRUE)+sd(df$V3,na.rm = TRUE),col="blue",lty=3)
abline(h=median(df$V3,na.rm=TRUE),col="green",lty=4)

#Identify the outliers
limit_v3=mean(df$V3,na.rm=TRUE)+sd(df$V3,na.rm = TRUE)
df$V3[df$V3>limit_v3 & !is.na(df$V3)]

#For outliers identification you can use the function identier to identify graphically the outliers
outliers_v3=identify(df$V3)

#Boxplot with nominal value 
bwplot(V2~V4,data = df, xlab = "V4 values", ylab = "V2 values")
bwplot(V2~V16,data = df, xlab = "V16 values", ylab = "V2 values")

#Missing preprocessing

#Delete all row with missing value
df_clean=na.omit(df)

#Replace the missing value with default value as median
df_clean1=df

#Replace with median
df_clean1$V2[is.na(df_clean1$V2)]=median(df$V2, na.rm=TRUE)

#Replace with modale value
#1
modale_value=names(which(table(df$V1)==max(table(df$V1))))
df_clean1$V1[is.na(df_clean1$V1)]=modale_value[1]
#2
modale_value=names(which(table(df$V4)==max(table(df$V4))))
df_clean1$V4[is.na(df_clean1$V4)]=modale_value[1]
#3
modale_value=names(which(table(df$V5)==max(table(df$V5))))
df_clean1$V5[is.na(df_clean1$V5)]=modale_value[1]
#4
modale_value=names(which(table(df$V6)==max(table(df$V6))))
df_clean1$V6[is.na(df_clean1$V6)]=modale_value[1]
#5
modale_value=names(which(table(df$V7)==max(table(df$V7))))
df_clean1$V7[is.na(df_clean1$V7)]=modale_value[1]

#Replace the missing value with regression prediction

#First, test the correlation between numerical variables with no missing values and variables with missing values.
cor.test(df_clean1$V3,df_clean1$V14,na.rm=TRUE)
cor.test(df_clean1$V8,df_clean1$V14,na.rm=TRUE)
cor.test(df_clean1$V15,df_clean1$V14,na.rm=TRUE)

#Second, build a linear model with the chosen variable
coefs=lm(df_clean1$V14~df_clean1$V3+df_clean1$V15)
summary(coefs)

#Replace the missing value with a built linear model 
df_clean1$V14[is.na(df_clean1$V14)]<-coefs$coefficients[1]+coefs$coefficients[2]*df_clean1$V3[is.na(df_clean1$V14)]+coefs$coefficients[3]*df_clean1$V15[is.na(df_clean1$V14)]

#NB : Another method for obtaining the modal value
# My data
vec <- c("a", "a", "b", "c", "c")

# Create a frequences table
table(vec)

# get the list of modal values
names(table(vec))[table(vec) == max(table(vec))]
names(which(table(vec)==max(table(vec))))
