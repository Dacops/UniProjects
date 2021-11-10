# representacao [(d,m,a)] = {'dia':d, 'mes':m, 'ano':a}

def cria_data(d,m,a):
    return '{}/{}/{}'.format(d,m,a)

def dia(dt):
    dt = dt.split('/')
    return eval(dt[0])

def mes(dt):
    dt = dt.split('/')
    return eval(dt[1])

def ano(dt):
    dt = dt.split('/')
    return eval(dt[2])

def eh_data(arg):
    arg = arg.split('/')
    if len(arg)!=3:
        return False
    return True

def mesma_data(d1,d2):
    if dia(d1)==dia(d2) and mes(d1)==mes(d2) and ano(d1)==ano(d2):
        return True
    return False

def escreve_data(data):
    d,m,a = dia(data),mes(data),ano(data)
    if len(str(dia(data)))==1:
        d='0'+str(dia(data))
    if len(str(mes(data)))==1:
        m='0'+str(mes(data))
    if ano(data)<0:
        a=str(ano(data))[1:]+' AC'
    return '{}/{}/{}'.format(d,m,a)

def data_anterior(d1,d2):
    if ano(d1)>ano(d2):
        return False
    if mes(d1)>mes(d2) and ano(d1)==ano(d2):
        return False
    if dia(d1)>dia(d2) and mes(d1)==mes(d2) and ano(d1)==ano(d2):
        return False
    return True

def idade(d1,d2):
    if data_anterior(d1,d2)==False:
        raise ValueError('idade: a pessoa ainda não nasceu.')
    dif = ano(d2)-ano(d1)
    if mes(d1)<mes(d2) or (mes(d1)==mes(d2) and dia(d1)<dia(d2)):
        dif += 1
    return dif
