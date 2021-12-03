import ex5

meses = ('jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez')
mes31 = ('jan', 'mar', 'mai', 'jul', 'ago', 'out', 'dez')
mes30 = ('abr', 'jun', 'set', 'nov')

def dias_mes(mes, ano):
    if mes not in meses:
        raise ValueError(' Mes não existe')

    if mes in mes31:
        return 31

    if mes in mes30:
        return 30

    else:
        if ex5.bissexto(ano)==True:
            return 29
        else:
            return 28
        

mes, ano = input('Mes: '), int(input('Ano: '))
print(dias_mes(mes, ano))