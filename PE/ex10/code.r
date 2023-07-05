set.seed(1340)  # Fixar a semente
mu <- 47.6   # Valor esperado sob a hipótese nula
sigma <- 2   # Desvio padrão (raiz quadrada da variância)
alpha <- 0.02  # Nível de significância
m <- 250    # Número de amostras
n <- 28     # Tamanho da amostra

reject <- rep(FALSE, m)  # Vetor para armazenar os resultados do teste

for (i in 1:m) {
  sample <- rnorm(n, mean = 48.7, sd = sigma)
  xbar <- mean(sample)  # Média da amostra i
  test_stat <- sqrt(n) * (xbar - mu) / sd(sample)  # Estatística de teste (z-score)
  p_value <- 2 * pt(abs(test_stat), df = n - 1, lower.tail = FALSE)  # Valor-p bilateral (duas caudas)
  reject[i] <- p_value < alpha  # Verificar se rejeita ou não a hipótese nula
}
prob_non_reject <- mean(!reject)
print(round(prob_non_reject, 3))