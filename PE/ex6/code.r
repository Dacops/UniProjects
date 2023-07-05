benford <- function(digit) {
    probability <- log10(1 + 1 / digit)
    return(probability)
}

ben_prob <- benford(4) + benford(9)

powers <- 2^(5:27)

check_first_digit <- function(number) {
    dig <- substr(number, 1, 1)
    return(dig == "4" || dig == "9")
}

count <- sum(sapply(powers, check_first_digit))

frac <- count / length(powers)

result <- abs(frac - ben_prob)

print(round(result, 4))
