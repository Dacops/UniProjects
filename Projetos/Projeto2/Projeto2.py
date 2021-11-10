# David Pires - ist1103458
# david.c.pires@tecnico.ulisboa.pt



###############
#     TAD     #
#   Posicao   #
###############

# Representacao: posicao = {'x':x, 'y':y}
# cria_posicao: int × int → posicao
# cria_copia_posicao: posicao → posicao
# obter_pos x: posicao → int
# obter_pos y: posicao → int
# eh_posicao: universal → booleano
# posicoes_iguais: posicao × posicao → booleano
# posicao_para_str: posicao → str


def cria_posicao(x,y):
    """
    int × int → posicao
    Recebe os valores correspondentes as coordenadas de uma posicao e devolve a posicao correspondente
    da forma interna da posicao: {'x':x, 'y':y}.
    O construtor verifica a validade dos seus argumentos, gerando um ValueError com a mensagem 
    'cria posicao:argumentos invalidos' caso os seus argumentos nao sejam validos.
    """
    if (type(x)!=int or 
        type(y)!=int or
        x<0 or y<0):
        raise ValueError('cria_posicao: argumentos invalidos')
    return {'x':x, 'y':y}


def cria_copia_posicao(p):
    """
    cria_copia_posicao: posicao → posicao
    Recebe uma posicao e devolve uma copia nova da posicao.
    """
    return {'x':p['x'], 'y':p['y']}


def obter_pos_x(p):
    """
    obter_pos x: posicao → int
    Devolve a componente 'x' da posicao 'p'.
    """
    return p['x']


def obter_pos_y(p):
    """
    obter_pos y: posicao → int
    Devolve a componente 'y' da posicao 'p'.
    """
    return p['y']


def eh_posicao(p):
    """
    eh_posicao: universal → booleano
    Devolve 'True' caso o seu argumento seja um TAD posicao e 'False' caso contrario.
    """
    # Verificacao da existencia, tipo e tamanho dos campos do argumento
    if(type(p)==dict and
       len(p)==2 and
       'x' in p and
       'y' in p and
       type(p['x'])==int and
       type(p['y'])==int and
       p['x']>=0 and p['y']>=0):
       return True
    return False


def posicoes_iguais(p1, p2):
    """
    posicoes_iguais: posicao × posicao → booleano
    Devolve True apenas se 'p1' e 'p2' sao posicoes e sao iguais.
    """
    if(eh_posicao(p1) and
       eh_posicao(p2) and        
       p1['x']==p2['x'] and
       p1['y']==p2['y']):
       return True
    return False


def posicao_para_str(p):
    """
    posicao_para_str: posicao → str
    Devolve a cadeia de caracteres '(x, y)' que representa o seu argumento,
    sendo os valores 'x' e 'y' as coordenadas de 'p'.
    """
    return '({}, {})'.format(obter_pos_x(p), obter_pos_y(p))


def obter_posicoes_adjacentes(p):
    """
    obter_posicoes_adjacentes: posicao → tuplo
    Devolve um tuplo com as posicoes adjacentes ah posicao 'p', comecando pela posicao acima de 'p'
    e seguindo no sentido horario.
    """
    pa1=cria_copia_posicao(cria_posicao(p['x'], p['y']-1)) if p['x']>=0 and p['y']-1>=0 else None
    pa2=cria_copia_posicao(cria_posicao(p['x']+1, p['y'])) if p['x']+1>=0 and p['y']>=0 else None
    pa3=cria_copia_posicao(cria_posicao(p['x'], p['y']+1)) if p['x']>=0 and p['y']+1>=0 else None
    pa4=cria_copia_posicao(cria_posicao(p['x']-1, p['y'])) if p['x']-1>=0 and p['y']>=0 else None
    pad, pp = (pa1, pa2, pa3, pa4), ()
    for pa in pad:
        if eh_posicao(pa):
            pp += (pa, )
    return pp


def ordenar_posicoes(t):
    """
    ordenar_posicoes: tuplo → tuplo
    Devolve um tuplo contendo as mesmas posicoes do tuplo fornecido como argumento, 
    ordenadas de acordo com a ordem de leitura do prado.
    """
    t = sorted(t, key=lambda item:item.get('y'))
    coordenada_anterior, count = None, 0
    for coordenada in t:
        if coordenada_anterior!=None:
            if coordenada['y']==coordenada_anterior['y']:
                coordenadas = [coordenada, coordenada_anterior]
                coordenadas = sorted(coordenadas, key=lambda item:item.get('x'))
                t = t[:count-1] + list(coordenadas) + t[count+1:]
        coordenada_anterior, count = coordenada, count+1
    return t



##############
#    TAD     #
#   Animal   #
##############

# Representacao: animal = {'especie':s, 'f_rep':r, 'f_ali':a, 'idade':0, 'fome':0}
# cria_animal: str × int × int → animal
# cria_copia_animal: animal → animal
# obter_especie: animal → str
# obter_freq_reproducao: animal → int
# obter_freq_alimentacao: animal → int
# obter_idade: animal → int
# obter_fome: animal → int
# aumenta_idade: animal → animal
# reset_idade: animal → animal
# aumenta_fome: animal → animal
# reset_fome: animal → animal
# eh_animal: universal → booleano
# eh_predador: universal → booleano
# eh_presa: universal → booleano
# animais_iguais: animal × animal → booleano
# animal_para_char: animal → str
# animal_para_str : animal → str


def cria_animal(s, r, a):
    """
    cria_animal: str × int × int → animal
    Recebe uma cadeia de caracteres 's' nao vazia correspondente ah especie do animal e dois valores inteiros 
    correspondentes ah frequencia de reproducao 'r' e ah frequencia de alimentacao 'a' e devolve o animal
    da forma interna do animal: {'especie':str, 'f_rep':int, 'f_ali':int, 'idade':int, 'fome':int}
    ('idade' e 'fome' tomam valor '0' nesta funcao).
    O construtor tambem verifica a validade dos seus argumentos, gerando um ValueError com a mensagem 
    'cria animal: argumentos invalidos' caso os seus argumentos nao sejam validos.
    """
    # Verificacao do tipo, tamanho dos argumentos
    if (type(s)!=str or
        str=='' or
        type(r)!=int or
        type(a)!=int or
        r<=0 or a<0):
        raise ValueError('cria_animal: argumentos invalidos')
    return {'especie':s, 'f_rep':r, 'f_ali':a, 'idade':0, 'fome':0}


def cria_copia_animal(a):
    """
    cria_copia_animal: animal → animal
    Recebe um animal 'a' (predador ou presa) e devolve uma nova copia do animal.
    """
    return {'especie':a['especie'], 'f_rep':a['f_rep'], 'f_ali':a['f_ali'], 'idade':a['idade'], 'fome':['fome']}


def obter_especie_animal(a):
    """
    obter_especie: animal → str
    Devolve a cadeia de caracteres correspondente ah especie do animal.
    """
    return a['especie']    


def obter_freq_reproducao(a):
    """
    obter_freq_reproducao: animal → int
    Devolve a frequencia de reproducao do animal 'a'.
    """
    return a['f_rep']    


def obter_freq_alimentacao(a):
    """
    obter_freq_alimentacao: animal → int
    Devolve a frequencia de alimentacao do animal 'a'.
    """
    return a['f_ali']    


def obter_idade(a):
    """
    obter_idade: animal → int
    Devolve a idade do animal 'a'.
    """
    return a['idade']


def obter_fome(a):
    """
    obter_fome: animal → int
    Devolve a fome do animal 'a'.
    """
    return a['fome']


def aumenta_idade(a):
    """
    aumenta_idade: animal → animal
    Modifica destrutivamente o animal 'a' incrementando o valor da sua idade em uma unidade, e devolve o proprio animal.
    """
    a['idade']=a['idade']+1
    return a


def reset_idade(a):
    """
    reset_idade: animal → animal
    Modifica destrutivamente o animal 'a' definindo o valor da sua idade igual a '0', e devolve o proprio animal.
    """
    a['idade']=0
    return a


def aumenta_fome(a):
    """
    aumenta_fome: animal → animal
    Modifica destrutivamente o animal predador 'a' incrementando o valor da sua fome em uma unidade, e devolve o proprio animal. 
    Esta operacao nao modifica os animais presa.
    """
    if eh_presa(a):
        pass
    if eh_predador(a):
        a['fome']=a['fome']+1
    return a


def reset_fome(a):
    """
    reset_fome: animal → animal
    Modifica destrutivamente o animal predador 'a' definindo o valor da sua fome igual a '0', e devolve o proprio animal. 
    Esta operacao nao modifica os animais presa.
    """
    a['fome']=0
    return a


def eh_animal(a):
    """
    eh_animal: universal → booleano
    Devolve 'True' caso o seu argumento seja um TAD animal e 'False' caso contrario.
    """
    if (type(a)!=dict or
        len(a)!=5 or

        # Verificacao de existencia dos campos do dicionario
        'especie' not in a or
        'f_rep' not in a or
        'f_ali' not in a or
        'idade' not in a or
        'fome' not in a or

        # Verificacao do tipo dos campos
        type(a['especie'])!=str or
        type(a['f_rep'])!=int or
        type(a['f_ali'])!=int or
        type(a['idade'])!=int or
        type(a['fome'])!=int or
        
        # Verificacao do tipo dos argumentos
        len(a['especie'])==0 or
        a['f_rep']<=0 or
        a['f_ali']<0 or
        a['idade']<0 or
        a['fome']<0):
        
        return False
    return True


def eh_predador(a):
    """
    eh_predador: universal → booleano
    Devolve 'True' caso o seu argumento seja um TAD animal do tipo predador e 'False' caso contrario.
    """
    if (eh_animal(a) and
        a['f_ali']>0):
        return True
    return False


def eh_presa(a):
    """
    eh_presa: universal → booleano
    Devolve 'True' caso o seu argumento seja um TAD animal do tipo presa e 'False' caso contrario.
    """
    if (eh_animal(a) and
        a['f_ali']==0):
        return True
    return False


def animais_iguais(a1, a2):
    """
    animais_iguais: animal × animal → booleano
    Devolve 'True' apenas se 'a1' e 'a2' sao animais e sao iguais.
    """
    if (eh_animal(a1) and               
        eh_animal(a2) and
        a1['especie']==a2['especie'] and
        a1['f_rep']==a2['f_rep'] and
        a1['f_ali']==a2['f_ali'] and
        a1['idade']==a2['idade'] and
        a1['fome']==a2['fome']):
        return True
    return False


def animal_para_char(a):
    """
    animal_para_char: animal → str
    Devolve a cadeia de caracteres dum unico elemento correspondente ao primeiro caracter da especie do animal 
    passada por argumento, em maiuscula para animais predadores e em minuscula para animais presa.
    """
    char = a['especie'][0]
    if eh_presa(a):
        return str(char.lower())
    if eh_predador(a):
        return str(char.upper())


def animal_para_str(a):
    """
    animal_para_str : animal → str
    Devolve a cadeia de caracteres que representa o animal como mostrado na sintaxe a seguir:
            - presa: 'especie [idade/f_rep]' 
            - predador: 'especie [idade/f_rep;fome/f_ali]'
    """
    if eh_presa(a):
        return '{} [{}/{}]'.format(a['especie'], a['idade'], a['f_rep'])
    if eh_predador(a):
        return '{} [{}/{};{}/{}]'.format(a['especie'], a['idade'], a['f_rep'], a['fome'], a['f_ali'])


def eh_animal_fertil(a):
    """
    eh_animal_fertil: animal → booleano
    Devolve 'True' caso o animal 'a' tenha atingido a idade de reproducao e 'False' caso contrario.
    """
    if obter_freq_reproducao(a)==obter_idade(a):
        return True
    else:
        return False


def eh_animal_faminto(a):
    """
    eh_animal_faminto: animal → booleano
    Devolve 'True' caso o animal 'a' tenha atingindo um valor de fome igual ou superior ah sua frequencia de alimentacao 
    e 'False' caso contrario. As presas devolvem sempre 'False'.
    """
    if eh_presa(a):
        return False
    if eh_predador(a):
        if obter_freq_alimentacao(a)<=obter_fome(a):
            return True
        else:
            return False


def reproduz_animal(a):
    """
    reproduz_animal: animal → animal
    Recebe um animal 'a' devolvendo um novo animal da mesma especie com idade e fome igual a '0',  
    modificando destrutivamente o animal passado como argumento 'a' alterando a sua idade para '0'.
    """
    n_a = cria_copia_animal(a)
    n_a = reset_fome(n_a)
    n_a = reset_idade(n_a)
    a = reset_idade(a)
    return n_a



###########
#   TAD   #
#  Prado  #
###########

# Representacao: prado = {'limite':d, 'rochas':r, 'animais':a, 'coords':p}
# cria_prado: posicao × tuplo × tuplo × tuplo → prado
# cria_copia_prado: prado → prado
# obter_tamanho_x: prado → int
# obter_tamanho_y: prado → int
# obter_numero_predadores: prado → int
# obter_numero_presa: prado → int
# obter_posicao_animais: prado → tuplo posicoes
# obter_animal: prado × posicao → animal
# eliminar_animal: prado × posicao → prado
# mover_animal: prado × posicao × posicao → prado
# inserir_animal: prado × animal × posicao → prado
# eh_prado: universal → booleano
# eh_posicao_animal: prado × posicao → booleano
# eh_posicao_obstaculo: prado × posicao → booleano
# eh_posicao_livre: prado × posicao → booleano
# prados_iguais: prado × prado → booleano
# prado_para_str: prado → str


def cria_prado(d, r, a, p):
    """
    cria_prado: posicao × tuplo × tuplo × tuplo → prado
    Recebe:
        -Uma posicao 'd' correspondente ah posicao que ocupa a montanha do canto inferior direito do prado,
        -Um tuplo 'r' de 0 ou mais posicoes correspondentes aos rochedos que nao sao as montanhas dos limites exteriores do prado,
        -Um tuplo 'a' de 1 ou mais animais, 
        -Um tuplo 'p' da mesma dimensao do tuplo 'a' com as posicoes correspondentes ocupadas pelos animais.

    Devolve o prado que representa internamente o mapa e os animais presentes. 
    O construtor verifica tambem a validade dos seus argumentos, gerando um ValueError com a mensagem
    'cria prado: argumentos invalidos' caso os seus argumentos nao sejam validos.
    """
    if (eh_posicao(d) and
       (eh_posicao(rocha) for rocha in r) and
       (eh_animal(animal) for animal in a) and
       (eh_posicao(coord) for coord in p)):
       return {'limite':d, 'rochas':r, 'animais':a, 'coords':p}
    raise ValueError('cria_prado: argumentos invalidos')


def cria_copia_prado(m):
    """
    cria_copia_prado: prado → prado
    Recebe um 'prado' e devolve uma nova copia do 'prado'.
    """
    return {'limite':m['limite'], 'rochas':m['rochas'], 'animais':m['animais'], 'coords':m['coords']}


def obter_tamanho_x(m):
    """
    obter_tamanho_x: prado → int
    Devolve o valor inteiro que corresponde ah dimensao 'x' do prado.
    """
    if 'limite' in m:
        return obter_pos_x(m['limite'])+1


def obter_tamanho_y(m):
    """
    obter_tamanho_y: prado → int
    Devolve o valor inteiro que corresponde ah dimensao 'y' do prado.
    """
    if 'limite' in m:
        return obter_pos_y(m['limite'])+1


def obter_numero_predadores(m):
    """
    obter_numero_predadores: prado → int
    Devolve o numero de animais predadores no prado.
    """
    return (eh_predador(animal) for animal in m['animais'])


def obter_numero_presas(m):
    """
    obter_numero_presas: prado → int
    Devolve o numero de animais presas no prado.
    """
    return (eh_presa(animal) for animal in m['animais'])


def obter_posicoes_animais(m):
    """
    obter_posicao_animais: prado → tuplo posicoes
    Devolve um tuplo contendo as posicoes do prado ocupadas por animais, ordenadas em ordem de leitura do prado.
    """
    return (ordenar_posicoes(posicao) for posicao in m['coords'])


def obter_animal(m, p):
    """
    obter_animal: prado × posicao → animal
    Devolve o animal do prado que se encontra na posicao 'p'.
    """
    count = -1
    for posicao in m['coords']:
        count += 1
        if p==posicao:
            return m['animais'][count]
    return None
    


def eliminar_animal(m, p):
    """
    eliminar_animal: prado × posicao → prado
    Modifica destrutivamente o prado 'm' eliminando o animal da posicao 'p' deixando-a livre. Devolve o proprio prado.
    """
    animais, posicoes = list(m['animais']), list(m['coords'])
    count = -1
    for posicao in posicoes:
        count += 1
        if posicao==p:
            break

    del animais[count]
    del posicoes[count]
    m['animais'], m['coords'] = tuple(animais), tuple(posicoes)
    return m


def mover_animal(m, p1, p2):    
    """
    mover_animal: prado × posicao × posicao → prado
    Modifica destrutivamente o prado 'm' movimentando o animal da posicao 'p1' para a nova posicao 'p2', deixando livre
    a posicao onde se encontrava. Devolve o proprio prado.
    """
    posicoes = list(m['coords'])
    count = 0
    for posicao in posicoes:
        if p1==posicao:
            posicoes[count] = p2
        count += 1
    m['coords']=tuple(posicoes)


def inserir_animal(m, a, p):
    """
    inserir_animal: prado × animal × posicao → prado
    Modifica destrutivamente o prado 'm' acrescentando na posicao 'p' do prado o animal 'a' passado com argumento.
    Devolve o proprio prado.
    """
    m['animais'] = m['animais'] + (a, )
    m['coords'] = m['coords'] + (p, )
    return m


def eh_prado(m):
    """
    eh_prado: universal → booleano
    Devolve 'True' caso o seu argumento seja um TAD prado e 'False' caso contrario.
    """
    #{'limite':d, 'rochas':r, 'animais':a, 'coords':p}
    if (type(m)!=dict or
        len(m)!=4 or

        # Existencia dos campos
        'limite' not in m or
        'rochas' not in m or
        'animais' not in m or
        'coords' not in m or

        # Validade dos campo
        eh_posicao(m['limite']) or
        (eh_posicao(rocha) for rocha in m['rochas']) or
        (eh_animal(animal) for animal in m['animais']) or
        (eh_posicao(posicao) for posicao in m['coords'])):

        return False
    return True


def eh_posicao_animal(m, p):
    """
    eh_posicao_animal: prado × posicao → booleano
    Devolve 'True' apenas no caso da posicao 'p' do prado estar ocupada por um animal.
    """
    if p in m['coords']:
        return True
    return False


def eh_posicao_obstaculo(m, p):
    """
    eh_posicao_obstaculo: prado × posicao → booleano
    Devolve 'True' apenas no caso da posicao 'p' do prado corresponder a uma montanha ou rochedo.
    """
    if p in m['rochas']:
        return True
    return False


def eh_posicao_livre(m, p):
    """
    eh_posicao_livre: prado × posicao → booleano
    Devolve 'True' apenas no caso da posicao 'p' do prado corresponder a um espaco livre (sem animais, nem obstaculos).
    """
    if eh_posicao_obstaculo(m, p) or eh_posicao_animal(m, p):
        return False
    return True


def prados_iguais(p1, p2):
    """
    prados_iguais: prado × prado → booleano
    Devolve 'True' apenas se 'p1' e 'p2' forem prados e forem iguais.
    """
    if (eh_prado(p1) and
        eh_prado(p2) and
        p1['limite']==p2['limite'] and
        p1['rochas']==p2['rochas'] and
        p1['animais']==p2['animais'] and
        p1['coords']==p2['coords']):
        return True
    return False


def prado_para_str(m):
    """
    prado_para_str: prado → str
    Devolve uma cadeia de caracteres que representa o prado como mostrado nos exemplos.
    """
    cx, cy, prado = obter_tamanho_x(m), obter_tamanho_y(m), ''
    for y in range(cy):                                                  
        linha, existe = '', 0 

        # Caso particular, linha nao vazia
        for x in range(1, cx-1):
            count = 0
            if cria_posicao(x, y) in m['rochas']:
                existe = 1
                linha += '@'
            if cria_posicao(x, y) in m['coords']:
                existe = 1
                for i in m['coords']:
                    if cria_posicao(x,y)==i:
                        break
                    count+=1
                linha += str(animal_para_char(m['animais'][count]))
            if (cria_posicao(x,y) not in m['rochas'] and
                cria_posicao(x,y) not in m['coords']):
                linha += '.'
        if existe==1:
            prado+=('|{}|'.format(linha))+'\n'

        # Caso geral, linha vazia
        else:
            if y==0:
                prado+=('+{}+'.format('-'*(cx-2)))+'\n'
            if y==(cy-1):
                prado+=('+{}+'.format('-'*(cx-2)))
            if y!=0 and y!=(cy-1):
                prado+=('|{}|'.format(linha))+'\n'

    return prado


def obter_valor_numerico(m, p):
    """
    obter_valor_numerico: prado × posicao → int
    Devolve o valor numerico da posicao 'p' correspondente ah ordem de leitura no prado 'm'.
    """
    x, y, dx = obter_pos_x(p), obter_pos_y(p), obter_tamanho_x(m)
    return (y)*dx+x
    

def obter_posicoes_adjacentes_sorted(m, p):
    """
    obter_posicoes_adjacentes: prado × posicao → posicao
    Devolve a posicao adjacente para qual o animal move, de acordo com as regras de movimento.
    FUNCAO LIGEIRAMENTE MODIFICADA (de obter_posicoes-adjacentes) PARA SER UTILIZADA EM OBTER_MOVIMENTO
    """
    # constraints unicas desta funcao
    pa1=cria_copia_posicao(cria_posicao(p['x'], p['y']-1)) if p['x']>0 and p['y']-1>0 and p['x']<obter_tamanho_x(m)-1 and p['y']-1<obter_tamanho_y(m)-1 and eh_posicao_livre(m, cria_posicao(p['x'], p['y']-1)) else None
    pa2=cria_copia_posicao(cria_posicao(p['x']+1, p['y'])) if p['x']+1>0 and p['y']>0 and p['x']+1<obter_tamanho_x(m)-1 and p['y']<obter_tamanho_y(m)-1 and eh_posicao_livre(m, cria_posicao(p['x']+1, p['y'])) else None
    pa3=cria_copia_posicao(cria_posicao(p['x'], p['y']+1)) if p['x']>0 and p['y']+1>0 and p['x']<obter_tamanho_x(m)-1 and p['y']+1<obter_tamanho_y(m)-1 and eh_posicao_livre(m, cria_posicao(p['x'], p['y']+1)) else None
    pa4=cria_copia_posicao(cria_posicao(p['x']-1, p['y'])) if p['x']-1>0 and p['y']>0 and p['x']-1<obter_tamanho_x(m)-1 and p['y']<obter_tamanho_y(m)-1 and eh_posicao_livre(m, cria_posicao(p['x']-1, p['y'])) else None
    pad, pp = (pa1, pa2, pa3, pa4), ()
    for pa in pad:
        if eh_posicao(pa):
            pp += (pa, )
    return pp


def obter_movimento(m, p):
    """
    obter_movimento: prado × posicao → posicao
    Devolve a posicao seguinte do animal na posicao 'p' dentro do prado 'm' de acordo com as regras de movimento dos animais no prado.
    """
    animal = obter_animal(m, p)
    n = obter_valor_numerico(m, p)
    l = len(obter_posicoes_adjacentes_sorted(m, p))

    if eh_presa(animal):
        coord_ad = obter_posicoes_adjacentes_sorted(m, p)
        if len(coord_ad)!=0:
            return coord_ad[n%l]
        return p
    if eh_predador(animal):
        coord_ad = obter_posicoes_adjacentes_sorted(m, p)
        # posicoes adjacentes, procura por presa
        for coord in coord_ad:
            if (eh_posicao_animal(m, coord) and eh_presa(obter_animal(m, coord))):
                return coord
        if len(coord_ad)!=0:
            return coord_ad[n%l]
        return p



#################
#    FUNCOES    #
#  ADICIONAIS   #
#################

# Utilizam grande parte das operacoes basicas definidas nas linhas acima de forma a criar simulacoes de diferentes
# geracoes de diferentes prados. Utilizando as regras definidas para simulacao de ecossistemas.

def geracao(m):
    """
    geracao: prado → prado
    Eh a funcao auxiliar que modifica o prado 'm' fornecido como argumento de acordo com a evolucao correspondente
    a uma geracao completa, e devolve o proprio prado. Isto eh, seguindo a ordem de leitura do prado, cada animal 
    (vivo) realiza o seu turno de acao de acordo com as regras descritas.
    """
    # De forma que "prado" não seja variavel local e prossiga para a proxima geracao
    global prado
    # Cria uma copia do prado, um prado é verificado e o outro alterado, de forma a que um prado não seja atualizado 
    # com dados inseridos nessa geracao.
    prado = cria_copia_prado(m)

    for y in range(obter_tamanho_y(m)):
        for x in range(obter_tamanho_x(m)):
            p = cria_posicao(x,y)
            if eh_posicao_animal(m, p):
                a = obter_animal(prado, p)
                mov = obter_movimento(prado, p)
                aumenta_idade(a)
                
                # Caso particular animal é predador
                if eh_predador(obter_animal(m, p)):
                    aumenta_fome(a)
                    # Verificar a fome do animal
                    if eh_animal_faminto(a):
                        eliminar_animal(prado, p)
                    # Se o predador comer uma presa
                    if eh_presa(obter_animal(prado, mov)):
                        eliminar_animal(prado, mov)
                        reset_fome(a)
                        mover_animal(prado, p, mov)
                    # Se o predador apenas se mover
                    if eh_posicao_livre(prado, mov):
                        # Verificar a fertilidade do animal
                        if not eh_animal_fertil(a):
                            mover_animal(prado, p, mov)
                        if eh_animal_fertil(a):
                            mover_animal(prado, p, mov)
                            inserir_animal(prado, reproduz_animal(obter_animal(prado, mov)), p)
                            

                # Caso particular animal é presa
                if eh_presa(obter_animal(m, p)):      
                    # Verificar a fertilidade do animal
                    if not eh_animal_fertil(a):
                        mover_animal(prado, p, mov)
                    if eh_animal_fertil(a):
                        mover_animal(prado, p, mov)
                        inserir_animal(prado, reproduz_animal(obter_animal(prado, mov)), p)
    return prado


def simula_ecossistema(f,g,v):
    """
    Eh a funcao principal que permite simular o ecossistema de um prado. A funcao recebe uma cadeia de caracteres f,
    um valor inteiro g e um valor booleano v e devolve o tuplo de dois elementos correspondentes ao numero de predadores e
    presas no prado no fim da simulacao. A cadeia de caracteres f passada por argumento corresponde ao nome do ficheiro de
    configuracao da simulacao. O valor inteiro g corresponde ao numero de geracoes a simular. O argumento booleano v ativa 
    o modo verboso (True) ou o modo quiet (False). No modo quiet mostra-se pela saida standard o prado, o numero de animais
    e o numero de geracao no inıcio da simulacao e apos a ultima geracao. No modo verboso, apos cada geracao, mostra-se tambem
    o prado, o numero de animais e o numero de geracao, apenas se o numero de animais predadores ou presas se tiver alterado.
    """
    # Interpretaçao de config
    config = open(f, 'r')
    full_config = config.readlines()

    # Por default, open da return de str, transformacao em tuples
    for i in range(len(full_config)):
        full_config[i]=eval(full_config[i])

    # Obtencao do limite do prado
    limite = cria_posicao(full_config[0][0], full_config[0][1])

    # Obtencao das rochas
    rochas = ()
    for rocha in full_config[1]:
        rochas += (cria_posicao(rocha[0], rocha[1]), )

    # Obtencao de animais e respetivas coordenadas
    animais, coordenadas = (), ()
    for animal in full_config[2:]:
        animais += (cria_animal(animal[0], animal[1], animal[2]), )
        coordenadas += (cria_posicao(animal[3][0], animal[3][1]), )

    # Criacao de prado, argumento para geracao()
    global prado
    prado = cria_prado(limite, rochas, animais, coordenadas)

    # Simulacao de 'g' geracoes
    for i in range(g):
        # Geracao 0
        if i==0:
            pr, pre = 0, 0
            for animal in animais:
                if eh_presa(animal):
                    pr += 1
                if eh_predador(animal):
                    pre += 1
            print('Predadores: {} vs Presas: {} (Gen. {})'.format(pre,pr,0))
            print(prado_para_str(prado))
            presas_ant, predadores_ant, turno_ant = pr, pre, prado

        # Dah update a prado
        turno = geracao(prado)

        # Obtencao de numero de presas/predadores para o output
        presas, predadores = 0, 0
        for y in range(obter_tamanho_y(prado)):
            for x in range(obter_tamanho_x(prado)):
                if eh_predador(obter_animal(prado, cria_posicao(x,y))):
                    predadores += 1
                if eh_presa(obter_animal(prado, cria_posicao(x,y))):
                    presas += 1

        if presas_ant!=presas or predadores_ant!=predadores:
            if v==True:
                print('Predadores: {} vs Presas: {} (Gen. {})'.format(predadores,presas,i+1))
                print(prado_para_str(turno))

        if v==True and turno_ant==turno:
            return '({}, {})'.format(predadores,presas)

        if v==False and turno_ant==turno:
            print('Predadores: {} vs Presas: {} (Gen. {})'.format(predadores,presas,g))
            print(prado_para_str(turno))
            return '({}, {})'.format(predadores,presas)
            
        presas_ant, predadores_ant, turno_ant = presas, predadores, turno

print(simula_ecossistema('C:\\Users\\david\\OneDrive\\Desktop\\Uni\\Fprog\\Projetos\\Projeto2\\config.txt', 200, True))
