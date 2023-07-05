set.seed(1790)  # Fixar a semente em 1790

m <- 2746  # Número de amostras
n <- 16    # Dimensão das amostras

# Gerar amostras da população normal
population <- matrix(rnorm(m * n, mean = 0, sd = 1), nrow = m)

# Calcular soma dos quadrados para cada amostra
sum_of_squares <- apply(population, 1, function(x) sum(x^2))

# Calcular o quantil de probabilidade 0.21 da amostra
quantile_sample <- quantile(sum_of_squares, probs = 0.21, type = 2)

# Calcular o quantil correspondente à distribuição teórica
quantile_theoretical <- qchisq(0.21, df = n)

# Calcular a diferença em valor absoluto
diferenca <- abs(quantile_sample - quantile_theoretical)

# Arredondar o resultado para 4 casas decimais
diferenca_arredondada <- round(diferenca, 4)

# Imprimir o resultado
print(diferenca_arredondada)
