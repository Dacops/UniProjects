# set working directory
setwd("C:/Users/david/OneDrive/Desktop/UniAll/2-2/PE/Projeto/ex2")

# read the .csv file
data <- read.csv("data/TIME_USE_24092022.csv")

# remove data from "África do Sul" and non "Total" rows
local <- data[, 1]
gender <- data[, 3]
filtered_data <- subset(data, gender == "Mulheres")
filtered_data <- subset(filtered_data, local != "África do Sul")

# save "Outros" and "Trabalho não remunerado ou estudo" from data
occupation <- filtered_data[, 2]
outros <- subset(filtered_data, occupation == "Outros")
work <- subset(filtered_data, occupation == "Trabalho remunerado ou estudo")
outros_vals <- outros[, 4]
work_vals <- work[, 4]

# create boxplots (diagrama de extremos e quantis)
png("plots.png", width = 1000, height = 600)
par(mfcol = c(1, 2))
combined_vals <- c(work_vals, outros_vals)
ylim_range <- range(combined_vals)
boxplot(work_vals, ylim = ylim_range, main = "Boxplot Trabalho não Remunerado\n ou Estudo")
boxplot(outros_vals, ylim = ylim_range, main = "Boxplot Outros")


# save the plots
dev.off()