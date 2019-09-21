library(randomForest)
library(lattice)
library(ggplot2)
library(gridExtra)
library(tidyr)
library(caret)

video = read.csv("path-to-file", header=T)

str(video)
summary(video)

video$Ratingn <- as.numeric(as.character(factor(video$Rating, levels =c("E" ,"E10+", "T", "M"), labels = c(1,2,3,4))))

index <- sample(1:nrow(video),size = 0.7 * nrow(video)) 
video.train <- video[index,]
video.test <- video[-index,]
nrow(video.train)

## Linear Regression with numerical data only

#NA_Linear
video_na.lm <- lm(formula= log(NA_Sales+1) ~ Ratingn + User_Score + Critic_Score + Series + Multi, data=video.train)
summary(video_na.lm)

video_na.lmimp <- varImp(video_na.lm)
video_na.lmimp <- video_na.lmimp[order(-video_na.lmimp$Overall),, drop=FALSE]

video_na.test.predlm <- exp(predict(video_na.lm,video.test))-1

#EU_Linear
video_eu.lm <- lm(formula= log(EU_Sales+1) ~ Ratingn + User_Score + Critic_Score + Series + Multi, data=video.train)
summary(video_eu.lm)

video_eu.lmimp <- varImp(video_eu.lm)
video_eu.lmimp <- video_eu.lmimp[order(-video_eu.lmimp$Overall),, drop=FALSE]

video_eu.test.predlm <- exp(predict(video_eu.lm,video.test))-1

#JP_Linear
video_jp.lm <- lm(formula= log(JP_Sales+1) ~ Ratingn + User_Score + Critic_Score + Series + Multi, data=video.train)
summary(video_jp.lm)

video_jp.lmimp <- varImp(video_jp.lm)
video_jp.lmimp <- video_jp.lmimp[order(-video_jp.lmimp$Overall),, drop=FALSE]

video_jp.test.predlm <- exp(predict(video_jp.lm,video.test))-1

#Other_Linear
video_ot.lm <- lm(formula= log(Other_Sales+1) ~ Ratingn + User_Score + Critic_Score + Series + Multi, data=video.train)
summary(video_ot.lm)

video_ot.lmimp <- varImp(video_ot.lm)
video_ot.lmimp <- video_ot.lmimp[order(-video_ot.lmimp$Overall),, drop=FALSE]

video_ot.test.predlm <- exp(predict(video_ot.lm,video.test))-1



## Random Forest Regression with mixed type data

#NA_RF
video_na.rf <- randomForest(NA_Sales ~ Rating + Platform + Critic_Score + User_Score +
                           Genre + Series + Multi,
                         data = video.train, importance = TRUE, na.action=na.roughfix)
which.min(video_na.rf$mse)

video_na.rfimp <- as.data.frame(sort(importance(video_na.rf)[,1],decreasing = TRUE),optional = T)
names(video_na.rfimp) <- "NA video % Inc MSE"

video_na.test.predrf <- predict(video_na.rf,video.test)


#EU_RF
video_eu.rf <- randomForest(EU_Sales ~ Rating + Platform + Critic_Score + User_Score +
                              Genre + Series + Multi,
                            data = video.train, importance = TRUE, na.action=na.roughfix)
which.min(video_eu.rf$mse)

video_eu.rfimp <- as.data.frame(sort(importance(video_eu.rf)[,1],decreasing = TRUE),optional = T)
names(video_eu.rfimp) <- "EU video % Inc MSE"

video_eu.test.predrf <- predict(video_eu.rf,video.test)


#JP_RF
video_jp.rf <- randomForest(JP_Sales ~ Rating + Platform + Critic_Score + User_Score +
                              Genre + Series + Multi,
                            data = video.train, importance = TRUE, na.action=na.roughfix)
which.min(video_jp.rf$mse)

video_jp.rfimp <- as.data.frame(sort(importance(video_jp.rf)[,1],decreasing = TRUE),optional = T)
names(video_jp.rfimp) <- "JP video % Inc MSE"

video_jp.test.predrf <- predict(video_jp.rf,video.test)


#Other_RF
video_ot.rf <- randomForest(Other_Sales ~ Rating + Platform + Critic_Score + User_Score +
                              Genre + Series + Multi,
                            data = video.train, importance = TRUE, na.action=na.roughfix)
which.min(video_ot.rf$mse)

video_ot.rfimp <- as.data.frame(sort(importance(video_ot.rf)[,1],decreasing = TRUE),optional = T)
names(video_ot.rfimp) <- "Other video % Inc MSE"

video_ot.test.predrf <- predict(video_ot.rf,video.test)


## Variable Importance of All Region ##
#
# video.allpred <- data.frame(actual = video.test$NA_Sales,
#                             linear.regression = video.test.predlm,
#                             random.forest = video.test.predrf)
# video.allpred <- gather(video.allpred,key = model,value = predictions,2:3)


# temp1 <- ggplot(data = video.allpred,aes(x = actual, y = predictions)) + 
#   geom_point(colour = "blue") + 
#   geom_abline(intercept = 0, slope = 1, colour = "red") +
#   facet_wrap(~ model,ncol = 2) + 
#   coord_cartesian(ylim = c(0, 6)) +
#   ggtitle("Video game Predicted and actual Data by model")


# grid.arrange(tableGrob(video_na.rfimp), tableGrob(video_eu.rfimp),
#              tableGrob(video_jp.rfimp), tableGrob(video_ot.rfimp),
#              top = "Variable Importance",
#              ncol=2)