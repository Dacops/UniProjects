set.seed(3418) # set seed
k <- 4106 # sample size
lambda <- 9 # parameter lambda
x <- rexp(k, lambda) # generate sample from exponential distribution
s <- cumsum(x) # calculate successive sum
T <- ceiling(s[k]) # calculate T
interval_count <- table(cut(s, breaks = seq(0, T, 1))) # count events in each interval
mean_count <- mean(interval_count) # calculate mean of event count per interval
expected_count <- lambda # expected value of event count per interval
deviation <- abs(mean_count - expected_count) # calculate absolute deviation
print(round(deviation, 4)) # round deviation to 4 decimal places