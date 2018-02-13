library(DBI)
library(RMySQL)
library(ggplot2)

con <- dbConnect(MySQL(), user="jaga663", password="chaos", host="10.111.49.49", dbname="Scouting2018")

query <- dbSendQuery(con, "SELECT * FROM matchdata")
data <- dbFetch(query, n=-1)
dbClearResult(query)

data$teamNumber <- as.factor(data$teamNumber)
head(data)
print(data)

switchBoxplot <- ggplot(data, aes(x=teamNumber, y=switch)) + geom_boxplot()
ggsave("plots/switch.png", switchBoxplot)

scaleBoxplot <- ggplot(data, aes(x=teamNumber, y=scale)) + geom_boxplot()
ggsave("plots/scale.png", scaleBoxplot)

exchangeBoxplot <- ggplot(data, aes(x=teamNumber, y=exchange)) + geom_boxplot()
ggsave("plots/exchange.png", exchangeBoxplot)
