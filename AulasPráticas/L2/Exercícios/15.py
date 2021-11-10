def soma(n):
    t = ''
    for i in range(len(n)-1):
        t += n[i]
    return t


n = input().split()
print(soma(n))