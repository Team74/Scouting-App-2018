library(DBI)
library(ggplot2)
library(envDocument)

con <- dbConnect(RSQLite::SQLite(), "display/r/graphdata.db")
con

print(dbListTables(con))
query <- dbSendQuery(con, "SELECT * FROM exchange")
data <- dbFetch(query, n=-1)
dbClearResult(query)

data$teamNumber <- as.factor(data$teamNumber) # who tf knows
head(data)
print(data)

switchBoxplot <-
  ggplot(data, aes(x=teamNumber, y=mean)) + geom_col(fill="steelblue", color="black") +
  geom_text(aes(label=mean), vjust=1.6, color="white", size=3.5) +
  geom_errorbar(aes(ymin=(mean-standev), ymax=(mean+standev)), width=.1)

ggsave("display/r/graphs/exchange.png", switchBoxplot)
