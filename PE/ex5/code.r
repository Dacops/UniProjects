set.seed(1900)
p <- 0.25
n <- 1104
u <- runif(n)
x <- numeric(n)
for (i in 1:n) {
  x[i] <- ceiling(log(1-u[i])/log(1-p)) - 1
}
mean_x <- mean(x)
sd_x <- sd(x)
prop <- mean(x > mean_x + sd_x & x > mean_x) 
print(round(prop, 4))
