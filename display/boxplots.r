library(DBI)
library(RSQLite)
library(ggplot2)

con = dbConnect(SQLite(), dbname="../scoutingdatabase.db")

query <- dbSendQuery(con, "SELECT * FROM matchdata")
data <- dbFetch(query, n=-1)
dbClearResult(query)

data$teamNumber <- as.factor(data$teamNumber)
head(data)
print(data)

switchBoxplot <- ggplot(data, aes(x=teamNumber, y=switch)) + geom_boxplot()
ggsave("plots/switch.png")

scaleBoxplot <- ggplot(data, aes(x=teamNumber, y=scale)) + geom_boxplot()
ggsave("plots/scale.png")

exchangeBoxplot <- ggplot(data, aes(x=teamNumber, y=exchange)) + geom_boxplot()
ggsave("plots/exchange.png")
