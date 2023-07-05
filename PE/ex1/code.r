# set working directory
setwd("C:/Users/david/OneDrive/Desktop/UniAll/2-2/PE/Projeto/ex2")

# load used packages
library(readxl)
library(ggplot2)

# read the excel sheet
data <- read_xlsx("data/econ.xlsx")

# filter data to only data after 1973
dates <- apply(data[, 1], 1, as.character)
years <- substr(dates, 1, 4)
filtered_data <- subset(data, years >= 1989)

# get the needed fields
time <- apply(filtered_data[, 1], 1, as.character)
pop <- apply(filtered_data[, 3], 1, as.numeric)
tpp <- apply(filtered_data[, 4], 1, as.numeric)

# transform the needed fields
tr_pop <- apply(matrix(pop, ncol = length(pop)), 1, function(x) (x - mean(pop)) / sd(pop))
tr_tpp <- apply(matrix(tpp, ncol = length(tpp)), 1, function(x) (x - mean(tpp)) / sd(tpp))

# create the graph
graph_data <- data.frame(x = time, y1 = tr_pop, y2 = tr_tpp)
ggplot(graph_data, aes(x = x, group = 1)) +
  geom_line(aes(y = y1), color = "red") +
  geom_line(aes(y = y2), color = "blue") +
  xlab("") + ylab("") +
  ggtitle("Evolution of pop and tpp since 1989") +
  annotate("text", x = 300, y = 3.25, label = "tpp", size = 5, color = "blue") +
  annotate("text", x = 300, y = 2.75, label = "pop", size = 5, color = "red")

# save the graph
ggsave("graph.png")