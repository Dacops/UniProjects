def soma(n):
    t = 0
    for i in range(len(n)):
        t += int(n[i])
    return t


n = input()
print(soma(n))