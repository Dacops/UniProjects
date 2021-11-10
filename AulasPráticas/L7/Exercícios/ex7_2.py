# relogio = [horas, minutos, segundos]

def cria_rel(h,m,s):
    return '{}:{}:{}'.format(h,m,s)

def horas(r):
    r=r.split(':')
    return eval(r[0])

def minutos(r):
    r=r.split(':')
    return eval(r[1])

def segs(r):
    r=r.split(':')
    return eval(r[2])

def eh_relogio(arg):
    arg.split(':')
    if len(arg)!=3:
        return False
    return True

def eh_meia_noite(r):
    if eval(horas(r))==0 and eval(minutos(r))==0 and eval(segs(r))==0:
        return True
    return False

def eh_meia_dia(r):
    if eval(horas(r))==12 and eval(minutos(r))==0 and eval(segs(r))==0:
        return True
    return False

def mesmas_horas(r1, r2):
    if horas(r1)==horas(r2) and minutos(r1)==minutos(r2) and segs(r1)==segs(r2):
        return True
    return False

def escreve_relogio(r):
    h = horas(r)
    if len(h)!=2:
        h='0'+horas(r)

    m = minutos(r)
    if len(minutos(r))!=2:
        m='0'+minutos(r)

    s = segs(r)
    if len(segs(r))!=2:
        s='0'+segs(r)
    return '{}:{}:{}'.format(h,m,s)

def depois_rel(r1, r2):
    if horas(r1)>horas(r2):
        return False
    if horas(r1)==horas(r2) and minutos(r1)>minutos(r2):
        return False
    if horas(r1)==horas(r2) and minutos(r1)==minutos(r2) and segs(r1)>segs(r2):
        return False
    return True

def dif_segs(r1, r2):
    if depois_rel(r1, r2)==False:
        raise ValueError('dif_segs: primeiro arg posterior ao segundo')
    h = abs(horas(r1)-horas(r2))*3600
    m = abs(minutos(r1)-minutos(r2))*60
    s = abs(segs(r1)-segs(r2))
    return h+m+s


