def corta(teste, saida, n):
    t = open(teste, 'r')
    s = open(saida, 'w')
    l = t.readlines()
    count, parte = 0, ''
    for linha in l:
        for caractere in linha:
            if count==n:
                s.write(parte)
            else:
                parte+=caractere
            count+=1
    s.write(parte)


if __name__=='__main__':
    print(corta('C:\\Users\\david\\OneDrive\\Desktop\\Uni\\Fprog\\AulasPráticas\\L8\\Ficheiros\\read.txt', 'C:\\Users\\david\\OneDrive\\Desktop\\Uni\\Fprog\\AulasPráticas\\L8\\Ficheiros\\write.txt', 20))