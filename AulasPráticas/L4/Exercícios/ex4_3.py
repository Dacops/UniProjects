def implode(n):
    string = ''
    for i in n:
        if type(i)!=int:
            raise ValueError('implode: elemento não inteiro')
        string += str(i)
    return string


if __name__ == '__main__':
    n = eval(input())
    print(implode(n))