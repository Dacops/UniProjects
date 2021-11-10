
def bissexto(ano):
    if (ano%4==0):
        if (ano%100==0):
            if (ano%400==0):
                return True
            else:
                return False

        return True

    else:
        return False


if __name__=='__main__':
    ano = int(input())
    print(bissexto(ano))