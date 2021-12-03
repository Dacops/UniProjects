"""
Projeto 1 de FP 2021/22
Aluno David Pires #103458
david.c.pires@tecnico.ulisboa.pt
"""


def corrigir_palavra(caracteres):
    """
    corrigir_palavra: cad. carateres → cad. carateres.
    Esta função corrige a palavra possivelmente modificada por um surto de letras.
    """
    ops = 1
    while ops!=0:
        anterior, count, ops = 0, 0, 0
        for letra in caracteres:
            if abs(ord(letra)-anterior)==32:
                caracteres = caracteres[:count-2*ops-1]+caracteres[count-2*ops+1:]
                ops += 1
                break
            anterior, count = ord(letra), count+1
    return caracteres



def eh_anagrama(palavra1, palavra2):
    """
    eh_anagrama: cad. carateres × cad. carateres → booleano.
    Esta função verifica se uma palavra é anagrama da outra.
    """
    simbolos1, simbolos2 = [], []
    for simbolo in palavra1:
        simbolos1.append(simbolo.upper())
    for simbolo in palavra2:
        simbolos2.append(simbolo.upper())
    simbolos1, simbolos2 = sorted(simbolos1), sorted(simbolos2)

    if simbolos1 != simbolos2:
        return False
    return True



def corrigir_doc(caracteres):
    """
    corrigir_doc: cad. carateres → cad. carateres.
    Esta função filtra uma cadeia de caracteres.
    """
    # no caso dos caracteres dados não serem iteráveis, por exemplo um inteiro
    if type(caracteres)!=str:
        raise ValueError('corrigir_doc: argumento invalido')

    valido, espaco = 1, 0
    for letra in caracteres:
        if letra.isalpha()==False and letra!=' ':
            valido = 0
        if letra == ' ':
            espaco += 1
        if espaco == 2:
                break
        if letra != ' ': 
            espaco = 0
    if len(caracteres) < 1 or valido == 0 or espaco == 2:
        raise ValueError('corrigir_doc: argumento invalido')
    
    caracteres = corrigir_palavra(caracteres)
    caracteres = caracteres.split()

    for palavra in caracteres:
        for palavra2 in caracteres:
            if palavra.upper() != palavra2.upper():
                if eh_anagrama(palavra, palavra2)==True:
                    caracteres.remove(palavra2)
    
    resultado = ''
    for i in caracteres:
        resultado += str(i) + ' '
    return resultado[:len(resultado)-1]
    



def obter_posicao(caracteres, inteiro):
    """
    obter_posicao: cad. carateres × inteiro → inteiro.
    Esta função devolve o inteiro correspondente à nova posição após o movimento.
    """
    movimentos, inteiro = {'B':'3', 'C':'-3', 'D':'1', 'E':'-1'}, int(inteiro)
    for movimento in caracteres:
        if (inteiro-1)%3==0 and movimento=='E':
            pass
        elif inteiro%3==0 and movimento=='D':
            pass
        elif (inteiro-4)<0 and movimento=='C':
            pass
        elif (inteiro+4)>10 and movimento=='B':
            pass
        else:
            inteiro += int(movimentos[movimento])
    return inteiro



def obter_digito(caracteres, inteiro):
    """
    obter_digito: cad. carateres × inteiro → inteiro.
    Esta função devolve o inteiro correspondente à nova posição após os movimentos.
    """
    # como já foi definida anteriormente
    return obter_posicao(caracteres, inteiro)



def obter_pin(movimentos):
    """
    obter_pin: tuplo → tuplo.
    Esta função devolve o pin codificado de acordo com os movimentos inseridos.
    """
    # verificar o tipo de input
    if type(movimentos)!=tuple:
        raise ValueError('obter_pin: argumento invalido')

    inteiro, pin, count, pertence, mov = 5, (), 0, 1, ('B', 'C', 'E', 'D')
    for caracteres in movimentos:
        if len(caracteres)<1:
            raise ValueError('obter_pin: argumento invalido')
        for caractere in caracteres:
            if caractere not in mov:
                raise ValueError('obter_pin: argumento invalido')
            
        inteiro = obter_posicao(caracteres, inteiro)
        pin += (inteiro, )
        count += 1
        
    if count<=3 or count>=11:
        raise ValueError('obter_pin: argumento invalido')
    return pin



def eh_entrada(sequencia):
    """
    eh_entrada: universal → booleano.
    Esta função verifica se foi inserida uma entrada BDB válida.
    """
    # no caso de algum campo inserido não fôr iterável
    try:
        # parametro geral
        if type(sequencia)!=tuple or len(sequencia)!=3:
            return False

        #parametros 1º campo
        if sequencia[0][0]=='-' or sequencia[0][-1]=='-':
            return False
        hifen = 0
        for caractere in sequencia[0]:
            if caractere=='-':
                if hifen==1:
                    return False
                hifen += 1
            else:
                hifen = 0
        palavras = sequencia[0].split('-')
        for palavra in palavras:
            for caractere in palavra:
                if caractere.isalpha()==False or caractere.isupper()==True:
                    return False
        if len(sequencia[0])<1:
            return False

        #parametros 2º campo
        count = 0
        if len(sequencia[1])!=7:
            return False
        for caractere in sequencia[1]:
            if (caractere!='[' and count==0) or (caractere!=']' and count==6):
                return False
            if count>0 and count<6:
                if caractere.isalpha()==False:
                    return False
            if count>6:
                return False
            count+=1

        #parametros 3º campo
        if type(sequencia[2])!=tuple or len(sequencia[2])<2:
            return False
        for numero in sequencia[2]:
            if type(numero)!=int or numero<0:
                return False
        return True

    except:
        return False



def validar_cifra(cifra, checksum):
    """
    validar_cifra: cad. carateres × cad. carateres → booleano.
    Esta função verifica se a sequência de controlo é coerente com a cifra.
    """
    # validação de argumentos não necessária

    # descodificacao
    # cria dicionario com letras da cifra e suas ocorrências
    letras = {}
    for letra in cifra:
        if letra in letras:
            letras[letra]+=1
        if letra not in letras and letra!='-':
            letras[letra]=1
    
    # se a letra com maior frequência não aparecer no "checksum"
    maior = max(letras, key=letras.get)
    if maior not in checksum:
        for letra in letras:
            if letras[maior] != letras[letra]:
                return False

    anterior, checksum, letra_anterior = letras[max(letras, key=letras.get)], checksum[1:len(checksum)-1], 'A'
    for letra in checksum:
        # Para que não exista traceback caso uma letra da cifra não esteja no dicionário criado
        try:
            if letras[letra]>anterior:
                return False
            if ord(letra_anterior)-ord(letra)>=0 and letras[letra_anterior]==letras[letra]:
                return False
        except:
            return False
        anterior, letra_anterior = letras[letra], letra
    return True



def filtrar_bdb(sequencia):
    """
    filtrar_bdb: lista → lista.
    Esta função filtra as entradas BDB não coerentes, devolvendo-as.
    """
    # no caso de o input não ser uma lista
    if type(sequencia)!=list:
        raise ValueError('filtrar_bdb: argumento invalido')

    if len(sequencia)==0:
        raise ValueError('filtrar_bdb: argumento invalido')
    for entrada in sequencia:
        if eh_entrada(entrada)==False:
            raise ValueError('filtrar_bdb: argumento invalido')

    erradas = []
    for campo in sequencia:
        if validar_cifra(campo[0], campo[1])==False:
            erradas.append(campo)
    return erradas



#eh_entrada já definida


def obter_num_seguranca(numeros):
    """
    obter_num_seguranca: tuplo → inteiro.
    Esta função devolve o número de segurança.
    """
    numeros, diferencas = sorted(list(numeros)), []
    for i in range(len(numeros)):
        # de forma a que o numeros[i+1] não saia do index
        try:
            diferenca = numeros[i+1]-numeros[i]
        except:
            pass
        diferencas.append(diferenca)
    resultados = sorted(list(diferencas))
    return resultados[0]



def decifrar_texto(caracteres, inteiro):
    """
    decifrar_texto: cad. carateres × inteiro → cad. carateres.
    Esta função devolve o texto decifrado.
    """
    inteiro, count, descodificado = inteiro%26, 0, ''
    for caractere in caracteres:
        espaco = 0
        if caractere == '-':
            descodificado += ' '
            espaco = 1
        if count%2==0:
            if ord(caractere)+inteiro+1>122:
                caractere = chr(97+((ord(caractere)+inteiro+1)-123))
            else:
                caractere = chr(ord(caractere)+inteiro+1)
        else:
            if ord(caractere)+inteiro-1>122:
                caractere = chr(97+(ord(caractere)+inteiro-1)-123)
            else:
                caractere = chr(ord(caractere)+inteiro-1)
        
        descodificado += caractere
        if espaco == 1:
            descodificado = descodificado[:len(descodificado)-1]
        
        count += 1
    return descodificado
        


def decifrar_bdb(lista):
    """
    decifrar_bdb: lista → lista.
    Esta função devolve as entradas BDB decifradas, na mesma ordem.
    """
    # no caso de o input dado não ser uma lista e por isso não iterável, por exemplo um inteiro
    if type(lista)!=list:
        raise ValueError('decifrar_bdb: argumento invalido')

    final = []
    for entrada in lista:
        if eh_entrada(entrada)==False:
            raise ValueError('decifrar_bdb: argumento invalido')

        texto = decifrar_texto(entrada[0], obter_num_seguranca(entrada[2]))
        final.append(texto)
    return final
 


def eh_utilizador(entrada):
    """
    eh_utilizador: universal → booleano.
    Esta função verifica se o utilizador inserido é válido.
    """
    # no caso de o dicionário não conter um dos seus campos
    try:
        if len(entrada['name'])<1 or len(entrada['pass'])<1 or len(entrada)!=3:
            return False
        if len(entrada['rule']['char'])>1 or type(entrada['rule']['vals'])!=tuple or len(entrada['rule']['vals'])!=2:
            return False

        # verificacao dos dados introduzidos em "rule""vals"
        if type(entrada['rule']['vals'][0])!=int or type(entrada['rule']['vals'][1])!=int:
            return False
        if entrada['rule']['vals'][0]<=0 or entrada['rule']['vals'][1]<=0:
            return False
        if entrada['rule']['vals'][0] > entrada['rule']['vals'][1]:
            return False
        return True
    except:
        return False



def eh_senha_valida(caracteres, dicionario):
    """
    eh_senha valida: cad. carateres × dicion´ario → booleano.
    Esta função verifica se a senha inserida é válida.
    """
    vogais, count, anterior, verifica, pertence = ('a', 'e', 'i', 'o', 'u'), 0, '', 0, 0
    for caractere in caracteres:
        if caractere.islower()==True and caractere in vogais:
            count += 1
        if caractere==dicionario['char']:
            pertence += 1
        if caractere==anterior:
            verifica = 1
        anterior = caractere

    if count>2 and verifica==1 and pertence>=dicionario['vals'][0] and pertence<=dicionario['vals'][1]:
        return True
    return False



def filtrar_senhas(lista):
    """
    filtrar_senhas: lista → lista.
    Esta função devolve a lista ordenada alfabeticamente com os nomes dos utilizadores com senhas erradas.
    """
    # no caso de o input dado não ser uma lista
    if type(lista)!=list:
        raise ValueError('filtrar_senhas: argumento invalido')

    utilizadores = []
    if len(lista)==0:
        raise ValueError('filtrar_senhas: argumento invalido')
    for entrada in lista:
        if eh_utilizador(entrada)==False:
            raise ValueError('filtrar_senhas: argumento invalido')
        if eh_senha_valida(entrada['pass'], entrada['rule'])==False:
            utilizadores.append(entrada['name'])

    utilizadores.sort()
    return utilizadores