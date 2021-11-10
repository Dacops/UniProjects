import ex5_5

def soma_mat(m1, m2):
    m = []
    for coluna in range(len(m1)):
        col = []
        for linha in range(len(m1[coluna])):
            col.append(m1[coluna][linha]+m2[coluna][linha])
        m.append(col)
    return ex5_5.matriz(m)
        

if __name__ == '__main__':
    m1, m2 = eval(input())
    print(soma_mat(m1, m2))