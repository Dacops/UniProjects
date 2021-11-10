def num_para_seq_cod(n):
    cod = ()
    for i in n:
        i = int(i)
        if i%2==0:
            i += 2
            i %= 10
        else:
            i -= 2
            i %= 10
        cod += (i, )
    return cod
        

if __name__ == '__main__':
    n = str(input())
    print(num_para_seq_cod(n))