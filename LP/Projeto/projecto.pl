%----------------------------%
%     David Pires, 103458    %
%   Primeiro Projeto de LP   %
%   Professora Luisa Coheur  %
%----------------------------%

%-------------------------------------------------------------------------------------------------------------------------%
% Notas:                                                                                                                  %
%  -> A primeira parte de cada variavel eh formada pelas iniciais da funcao a qual pertence, para melhor leitura,         %
%     e evitar problemas de unificacao, uma vez que funcoes definidas podem ser chamadas posteriormente.                  %
%  -> Meta-Predicados foram dados apos a iniciacao do projeto e por isso serao utilizados a partir do predicado 2.8.      %
%     (eh normal que o codigo inicial esteja 100x pior que o final devido ahj experiencia que adquiri em prolog durante   %
%     a realizacao do projeto).                                                                                           %
%-------------------------------------------------------------------------------------------------------------------------%


%------------------------------------------------------------------------------------------------------------------------%
% 2.1.extrai_ilhas_linha(EIL_NL, EIL_Linha, EIL_Ilhas):                                                                  %
%  -> EIL_NL, eh um  inteiro  positivo, correspondente ao numero de uma linha.                                           %
%  -> EIL_Linha, eh uma lista correspondente a uma linha de um puzzle.                                                   %
%  -> EIL_Ilhas, eh a lista ordenada (ilhas da esquerda para a direita) cujos elementos sao as ilhas da linha EIL_Linha. %
%------------------------------------------------------------------------------------------------------------------------%

extrai_ilhas_linha(EIL_NL, EIL_Linha, EIL_Ilhas) :- extrai_ilhas_linha(EIL_NL, EIL_Linha, EIL_Ilhas, 0, []), !.
extrai_ilhas_linha(_, [], EIL_Ilhas, _, EIL_Ilhas).
extrai_ilhas_linha(EIL_NL, [EIL_Cabeca|EIL_Cauda], EIL_Ilhas, EIL_Counter, EIL_AuxIlhas) :-
    EIL_Cabeca == 0, !,
    EIL_NCounter is +(EIL_Counter, 1),
    extrai_ilhas_linha(EIL_NL, EIL_Cauda, EIL_Ilhas, EIL_NCounter, EIL_AuxIlhas).
extrai_ilhas_linha(EIL_NL, [EIL_Cabeca|EIL_Cauda], EIL_Ilhas, EIL_Counter, EIL_AuxIlhas) :-
    EIL_NCounter is +(EIL_Counter, 1),
    append(EIL_AuxIlhas, [ilha(EIL_Cabeca, (EIL_NL, EIL_NCounter))], EIL_NIlhas),
    extrai_ilhas_linha(EIL_NL, EIL_Cauda, EIL_Ilhas, EIL_NCounter, EIL_NIlhas).


%------------------------------------------------------------------------------------------------------------------------------%
% 2.2.ilhas(I_Puz, I_Ilhas):                                                                                                   %
%  -> I_Puz, eh um puzzle.                                                                                                     %
%  -> I_Ilhas, eh a lista ordenada(ilhas da esquerda para a direita e de cima para baixo) cujos elementos sao as ilhas de Puz. % 
%------------------------------------------------------------------------------------------------------------------------------%

ilhas(I_Puz, I_Ilhas) :- ilhas(I_Puz, [], I_Ilhas, 0).
ilhas([], I_Ilhas, I_Ilhas, _).
ilhas([I_Cabeca|I_Cauda], I_ConjuntoIlhas, I_Ilhas, I_Counter) :-
    I_NCounter is +(I_Counter,1),
    extrai_ilhas_linha(I_NCounter, I_Cabeca, I_IlhasLinhaActual),
    append(I_ConjuntoIlhas, I_IlhasLinhaActual, I_NovoConjuntoIlhas),
    ilhas(I_Cauda, I_NovoConjuntoIlhas, I_Ilhas, I_NCounter).


%----------------------------------------------------------------------------------------------------------------------------------------------%
% 2.3.vizinhas(V_Ilhas, V_Ilha, V_Vizinhas):                                                                                                   %
%  -> V_Ilhas eh a lista de ilhas de um puzzle.                                                                                                %
%  -> V_Ilha eh uma dessas ilhas.                                                                                                              %
%  -> V_Vizinhas eh a lista ordenada (ilhas de cima para baixo e da esquerda para a direita ) cujos elementos sao as ilhas vizinhas de V_Ilha. %
%                                                                                                                                              %
% FUNCOES AUXILIARES:                                                                                                                          %
%  -> cima/baixo/esquerda/direita, transformam a lista de vizinhos nessa direcao apenas no vizinho mais proximo.                               %
%  -> {cima/baixo/esquerda/direita}_aux, utilizam algoritmos para obter o vizinho mais proximo.                                                %
%  -> return, dah return ah resposta.                                                                                                          %
%----------------------------------------------------------------------------------------------------------------------------------------------%

vizinhas(V_Ilhas, V_Ilha, V_Vizinhas) :- vizinhas(V_Ilhas, V_Ilha, [], [], [], [], [], V_Vizinhas), !.
vizinhas([], _, V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas) :-
    cima(V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas).
vizinhas([V_Cabeca|V_Cauda], V_Ilha, V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas) :-
    V_Ilha = ilha(_, (V_Y1, V_X1)),
    V_Cabeca = ilha(_, (V_Y2, V_X2)),
    V_X1 == V_X2, V_Y1 \== V_Y2,
    (V_Y1 > V_Y2, append(V_C, [V_Cabeca], V_NC), append(V_B, [], V_NB);
    V_Y1 < V_Y2, append(V_B, [V_Cabeca], V_NB), append(V_C, [], V_NC)),
    vizinhas(V_Cauda, V_Ilha, V_NC, V_E, V_D, V_NB, V_NVizinhas, V_Vizinhas).
vizinhas([V_Cabeca|V_Cauda], V_Ilha, V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas) :-
    V_Ilha = ilha(_, (V_Y1, V_X1)),
    V_Cabeca = ilha(_, (V_Y2, V_X2)),
    V_X1 \== V_X2, V_Y1 == V_Y2,
    (V_X1 < V_X2, append(V_D, [V_Cabeca], V_ND), append(V_E, [], V_NE); 
    V_X1 > V_X2, append(V_E, [V_Cabeca], V_NE), append(V_D, [], V_ND)),
    vizinhas(V_Cauda, V_Ilha, V_C, V_NE, V_ND, V_B, V_NVizinhas, V_Vizinhas).
vizinhas([_|V_Cauda], V_Ilha, V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas) :-
    vizinhas(V_Cauda, V_Ilha, V_C, V_E, V_D, V_B, V_NVizinhas, V_Vizinhas).

cima(C_C, C_E, C_D, C_B, C_NVizinhas, C_Vizinhas) :-
    C_C == [], append(C_NVizinhas, [], C_AUXVizinhas), esquerda(C_E, C_D, C_B, C_AUXVizinhas, C_Vizinhas);
    length(C_C, 1), append(C_NVizinhas, C_C, C_AUXVizinhas), esquerda(C_E, C_D, C_B, C_AUXVizinhas, C_Vizinhas);
    cima_aux(C_C, C_E, C_D, C_B, C_NVizinhas, C_Vizinhas).
cima_aux([_|CA_Cauda], CA_E, CA_D, CA_B, CA_NVizinhas, CA_Vizinhas) :-
    length(CA_Cauda, 1), append(CA_NVizinhas, CA_Cauda, CA_AUXVizinhas),
    esquerda(CA_E, CA_D, CA_B, CA_AUXVizinhas, CA_Vizinhas);
    cima_aux(CA_Cauda, CA_E, CA_D, CA_B, CA_NVizinhas, CA_Vizinhas).

esquerda(E_E, E_D, E_B, E_NVizinhas, E_Vizinhas) :-
    E_E == [], append(E_NVizinhas, [], E_AUXVizinhas), direita(E_D, E_B, E_AUXVizinhas, E_Vizinhas);
    length(E_E, 1), append(E_NVizinhas, E_E, E_AUXVizinhas), direita(E_D, E_B, E_AUXVizinhas, E_Vizinhas);
    esquerda_aux(E_E, E_D, E_B, E_NVizinhas, E_Vizinhas).
esquerda_aux([_|EA_Cauda], EA_D, EA_B, EA_NVizinhas, EA_Vizinhas) :-
    length(EA_Cauda, 1), append(EA_NVizinhas, EA_Cauda, EA_AUXVizinhas),
    direita(EA_D, EA_B, EA_AUXVizinhas, EA_Vizinhas);
    esquerda_aux(EA_Cauda, EA_D, EA_B, EA_NVizinhas, EA_Vizinhas).
    
direita(D_D, D_B, D_NVizinhas, D_Vizinhas) :-
    D_D == [], append(D_NVizinhas, [], D_AUXVizinhas), baixo(D_B, D_AUXVizinhas, D_Vizinhas);
    direita_aux(D_D, D_B, D_NVizinhas, D_Vizinhas).
direita_aux([DA_Cabeca|_], DA_B, DA_NVizinhas, DA_Vizinhas) :-
    append(DA_NVizinhas, [DA_Cabeca], DA_AUXVizinhas),
    baixo(DA_B, DA_AUXVizinhas, DA_Vizinhas).

baixo(B_B, B_NVizinhas, B_Vizinhas) :-
    B_B == [], append(B_NVizinhas, [], B_AUXVizinhas), return(B_AUXVizinhas, B_Vizinhas);
    baixo_aux(B_B, B_NVizinhas, B_Vizinhas).
baixo_aux([BA_Cabeca|_], BA_NVizinhas, BA_Vizinhas) :-
    append(BA_NVizinhas, [BA_Cabeca], BA_AUXVizinhas),
    return(BA_AUXVizinhas, BA_Vizinhas).

return(R_NVizinhas, R_Vizinhas) :- return(R_NVizinhas, R_Vizinhas, 1).
return(R_Vizinhas, R_Vizinhas, 0).
return(R_NVizinhas, R_Vizinhas, R_Counter) :-
    R_NCounter is -(R_Counter, 1),
    return(R_NVizinhas, R_Vizinhas, R_NCounter).


%--------------------------------------------------------------------------------------------------------------%
% 2.4.estado(E_Ilhas, E_Estado):                                                                               %
%  -> E_Ilhas eh a lista de ilhas de um puzzle.                                                                %
%  -> E_Estado eh a lista ordenada cujos elementos sao as entradas referentes a cada uma das ilhas de E_Ilhas. %
%--------------------------------------------------------------------------------------------------------------%

estado(E_Ilhas, E_Estado) :- estado(E_Ilhas, E_Ilhas, [], E_Estado).
estado([], _, E_Estado, E_Estado).
estado([E_Cabeca|E_Cauda], E_Ilhas, E_AUXEstado, E_Estado) :-
    vizinhas(E_Ilhas, E_Cabeca, X),
    append(E_AUXEstado, [[E_Cabeca, X, []]], E_NAUXEstado),
    estado(E_Cauda, E_Ilhas, E_NAUXEstado, E_Estado).


%-------------------------------------------------------------------------------------------------------------%
% 2.5.posicoes_entre(PE_Pos1, PE_Pos2, PE_Posicoes):                                                          %
%  -> PE_Pos1 eh PE_Pos2 sao posicoes.                                                                        %
%  -> PE_Posicoes eh a lista ordenada de posicoes entre PE_Pos1 e PE_Pos2 (excluindo PE_Pos1 e PE_Pos2).      %
%                                                                                                             %
% NOTA: Se PE_Pos1 e PE_Pos2 nao pertencerem ah mesma linha ou ah mesma coluna, o resultado eh false.         %
%                                                                                                             %
% FUNCOES AUXILIARES:                                                                                         %
%  -> avalia_posicoes{x/y}({X/Y}, {X/Y}1, {X/Y}2, PE_Posicoes):                                               %
%      -> cria a diferenca entre as coordenadas que se alteram, x ou y.                                       %
%      -> {X/Y} eh a coordenada que nao se altera entre as duas posicoes dadas como input.                    %
%      -> {X/Y}1, {X/Y}2, sao as coordenadas que se alteram, cada uma de um input.                            %
%      -> PE_Posicoes eh a lista ordenada de posicoes entre PE_Pos1 e PE_Pos2 (excluindo PE_Pos1 e PE_Pos2).  %
%  -> cria_posicoes{x/y}({X/Y}, {X/Y}1, {X/Y}, PE_Posicoes):                                                  %
%      -> {X/Y} eh a coordenada que nao se altera entre as duas posicoes dadas como input.                    %
%      -> {X/Y}1 eh a coordenada que se altera de maior valor entre as duas posicoes dadas como input.        %
%      -> {X/Y} eh a diferenca entre as coordenadas que se alteram das duas posicoes dadas como input.        %
%      -> PE_Posicoes eh a lista ordenada de posicoes entre PE_Pos1 e PE_Pos2 (excluindo PE_Pos1 e PE_Pos2).  %
%-------------------------------------------------------------------------------------------------------------%

posicoes_entre(PE_Pos1, PE_Pos2, PE_Posicoes) :-
    PE_Pos1 = (PE_X1, PE_Y1),
    PE_Pos2 = (PE_X2, PE_Y2),
    (PE_X1 == PE_X2, PE_Y1 \== PE_Y2), !,
    avalia_posicoesy(PE_X1, PE_Y1, PE_Y2, PE_Posicoes).
posicoes_entre(PE_Pos1, PE_Pos2, PE_Posicoes) :-
    PE_Pos1 = (PE_X1, PE_Y1),
    PE_Pos2 = (PE_X2, PE_Y2),
    (PE_X1 \== PE_X2, PE_Y1 == PE_Y2), !,
    avalia_posicoesx(PE_Y1, PE_X1, PE_X2, PE_Posicoes).

avalia_posicoesy(APY_X, APY_Y1, APY_Y2, APY_Posicoes) :-
    APY_Y1 > APY_Y2, !,
    APY_Y is -(APY_Y1, APY_Y2),
    cria_posicoesy(APY_X, APY_Y1, APY_Y, APY_Posicoes).
avalia_posicoesy(APY_X, APY_Y1, APY_Y2, APY_Posicoes) :-
    APY_Y1 < APY_Y2, !,
    APY_Y is -(APY_Y2, APY_Y1),
    cria_posicoesy(APY_X, APY_Y2, APY_Y, APY_Posicoes).

avalia_posicoesx(APX_Y, APX_X1, APX_X2, APX_Posicoes) :-
    APX_X1 > APX_X2, !,
    APX_X is -(APX_X1, APX_X2),
    cria_posicoesx(APX_Y, APX_X1, APX_X, APX_Posicoes).
avalia_posicoesx(APX_Y, APX_X1, APX_X2, APX_Posicoes) :-
    APX_X1 < APX_X2, !,
    APX_X is -(APX_X2, APX_X1),
    cria_posicoesx(APX_Y, APX_X2, APX_X, APX_Posicoes).

cria_posicoesy(CPY_X, CPY_Y1, CPY_Y, CPY_Posicoes) :- cria_posicoesy(CPY_X, CPY_Y1, CPY_Y, [], CPY_Posicoes), !.
cria_posicoesy(_, _, 1, CPY_Posicoes, CPY_Posicoes).
cria_posicoesy(CPY_X, CPY_Y1, CPY_Y, CPY_AUXPosicoes, CPY_Posicoes) :-
    CPY_NY is -(CPY_Y,1),
    CPY_NNY is -(CPY_Y1,CPY_NY),
    append(CPY_AUXPosicoes, [(CPY_X, CPY_NNY)], CPY_NAUXPosicoes),
cria_posicoesy(CPY_X, CPY_Y1, CPY_NY, CPY_NAUXPosicoes, CPY_Posicoes).

cria_posicoesx(CPX_Y, CPX_X1, CPX_X, CPX_Posicoes) :- cria_posicoesx(CPX_Y, CPX_X1, CPX_X, [], CPX_Posicoes), !.
cria_posicoesx(_, _, 1, CPX_Posicoes, CPX_Posicoes).
cria_posicoesx(CPX_Y, CPX_X1, CPX_X, CPX_AUXPosicoes, CPX_Posicoes) :-
    CPX_NX is -(CPX_X,1),
    CPX_NNX is -(CPX_X1,CPX_NX),
    append(CPX_AUXPosicoes, [(CPX_NNX, CPX_Y)], CPX_NAUXPosicoes),
cria_posicoesx(CPX_Y, CPX_X1, CPX_NX, CPX_NAUXPosicoes, CPX_Posicoes).


%----------------------------------------------------%
% 2.6.cria_ponte(Pos1, Pos2, Ponte):                 %
%  -> CP_Pos1 e CP_Pos2 sao 2 posicoes.              %
%  -> CP_Ponte eh uma ponte entre essas 2 posicoes.  %
%----------------------------------------------------%

cria_ponte(CP_Pos1, CP_Pos2, CP_Ponte) :- cria_ponte(1, CP_Pos1, CP_Pos2, [], CP_Ponte), !.
cria_ponte(0, _, _, CP_Ponte, CP_Ponte).
cria_ponte(CP_Counter, CP_Pos1, CP_Pos2, CP_AUXPonte, CP_Ponte) :-
    CP_NCounter is -(CP_Counter, 1),
    CP_Pos1 = (CP_X1, CP_Y1),
    CP_Pos2 = (CP_X2, CP_Y2),
    ((CP_X1<CP_X2, append(CP_AUXPonte, [ponte((CP_X1, CP_Y1), (CP_X2, CP_Y2))], CP_NAUXPonte);
    CP_X1>CP_X2, append(CP_AUXPonte, [ponte((CP_X2, CP_Y2), (CP_X1, CP_Y1))], CP_NAUXPonte));
    (CP_Y1<CP_Y2, append(CP_AUXPonte, [ponte((CP_X1, CP_Y1), (CP_X2, CP_Y2))], CP_NAUXPonte);
    CP_Y1>CP_Y2, append(CP_AUXPonte, [ponte((CP_X2, CP_Y2), (CP_X1, CP_Y1))], CP_NAUXPonte))),
    CP_NAUXPonte = [CP_NNAUXPonte],
    cria_ponte(CP_NCounter, CP_Pos1, CP_Pos2, CP_NNAUXPonte, CP_Ponte).


%--------------------------------------------------------------------------%
% 2.7.caminho_livre(CL_Pos1, CL_Pos2, CL_Posicoes, CL_I, CL_Vz):           %
%  -> CL_Pos1 CL_Pos2 sao posicoes.                                        %
%  -> CL_Posicoes eh a lista ordenada de posicoes entre CL_Pos1 e CL_Pos2. %
%  -> CL_I eh uma ilha.                                                    %
%  -> CL_Vz eh uma das suas vizinhas.                                      %
%--------------------------------------------------------------------------%

caminho_livre(CL_Pos1, CL_Pos2, CL_Posicoes, CL_I, CL_Vz) :-
    CL_I = ilha(_, (CL_X1, CL_Y1)),
    CL_Vz = ilha(_, (CL_X2, CL_Y2)),
    posicoes_entre((CL_X1, CL_Y1), (CL_X2, CL_Y2), CL_NPosicoes),
    ((CL_Pos1 == (CL_X1,CL_Y1), CL_Pos2 == (CL_X2,CL_Y2), !;
    CL_Pos1 == (CL_X2,CL_Y2), CL_Pos2 == (CL_X1,CL_Y1)), !;
    intersection(CL_Posicoes, CL_NPosicoes, [])), !.


%----------------------------------------------------------------------------------------------------------%
% 2.8.actualiza_vizinhas_entrada(AVE_Pos1, AVE_Pos2, AVE_Posicoes, AVE_Entrada, AVE_Nova_Entrada):         %
%  -> AVE_Pos1 e AVE_Pos2 sao as posicoes entre as quais irah ser adicionada uma ponte.                    %
%  -> AVE_Posicoes eh a lista ordenada de posicoes entre Pos1 e Pos2.                                      %
%  -> AVE_Entrada eh uma entrada.                                                                          %
%  -> AVE_Nova_Entrada eh igual a Entrada, excepto no que diz respeito ah lista de ilhas vizinhas,         %
%     esta deve ser actualizada, removendo as ilhas que deixaram de ser vizinhas, apos a adicao da ponte.  %
%----------------------------------------------------------------------------------------------------------%

actualiza_vizinhas_entrada(AVE_Pos1, AVE_Pos2, AVE_Posicoes, AVE_Entrada, AVE_Nova_Entrada) :-
    [AVE_I, AVE_Vz, AVE_Pontes] = AVE_Entrada,
    include(caminho_livre(AVE_Pos1, AVE_Pos2, AVE_Posicoes, AVE_I), AVE_Vz, AVE_NEntrada),
    AVE_Nova_Entrada = [AVE_I, AVE_NEntrada, AVE_Pontes].
    

%-------------------------------------------------------------------------------------------------------------------------------------%
% 2.9.actualiza_vizinhas_apos_pontes(AVAP_Estado, AVAP_Pos1, AVAP_Pos2, AVAP_Novo_estado):                                            %
%  -> AVAP_Estado eh um estado.                                                                                                       %
%  -> AVAP_Pos1 e AVAP_Pos2 sao as posicoes entre as quais foi adicionada uma ponte.                                                  %
%  -> AVAP_Novo_estado eh o estado que se obtem de AVAP_Estado apos a actualizacao das ilhas vizinhas de cada uma das suas entradas.  %
%-------------------------------------------------------------------------------------------------------------------------------------%

actualiza_vizinhas_apos_pontes(AVAP_Estado, AVAP_Pos1, AVAP_Pos2, AVAP_Novo_estado) :-
    posicoes_entre(AVAP_Pos1, AVAP_Pos2, AVAP_Posicoes),
    maplist(actualiza_vizinhas_entrada(AVAP_Pos1, AVAP_Pos2, AVAP_Posicoes), AVAP_Estado, AVAP_Novo_estado).


% --------------------------------------------------------------------------------------------------------------------------------%
% 2.10.ilhas_terminadas(IT_Estado, IT_Ilhas_term):                                                                                %
%  -> IT_Estado eh um estado.                                                                                                     %
%  -> IT_Ilhas_term eh a lista de ilhas que jah tem todas as pontes associadas, designadas por ilhas terminadas.                  %
%     Se a entrada referente a uma ilha for [ilha(N_pontes,Pos), Vizinhas, Pontes],  esta ilha estah terminada, se N_pontes for   %
%     diferente de 'X'(a razao para esta condicao ficarah aparente mais ah frente) e o comprimento da lista Pontes for N_pontes.  %
%                                                                                                                                 %
% FUNCOES AUXILIARES:                                                                                                             %
%  -> terminada(IT_Estado):                                                                                                       %
%      -> Funcao auxiliar para o include(), retira as ilhas terminadas.                                                           %
%  -> transforma(IT_NIlhas, IT_Goal):                                                                                             %
%      -> Funcao auxiliar para o maplist(), transforma a ilha na representacao pedida pelo enunciado.                             %
%---------------------------------------------------------------------------------------------------------------------------------%

ilhas_terminadas(IT_Estado, IT_Ilhas_term) :-
    include(terminada, IT_Estado, IT_NIlhas),
    maplist(transforma, IT_NIlhas, IT_Ilhas_term).
terminada(IT_Estado) :-
    IT_Estado = [ilha(X,_),_,Y],
    maplist(integer, [X]),
    length(Y, X).
transforma([IT_Cabeca|_], IT_Goal) :-
    IT_Goal = IT_Cabeca.


%-------------------------------------------------------------------------------------------------------------------------------%
% 2.11.tira_ilhas_terminadas_entrada(TITE_Ilhas_term, TITE_Entrada, TITE_Nova_entrada):                                         %
%  -> TITE_Ilhas_term eh uma lista de ilhas terminadas.                                                                         %
%  -> TITE_Entrada eh uma entrada.                                                                                              %
%  -> TITE_Nova_entrada eh a entrada resultante de remover as ilhas de TITE_Ilhas_term, da lista de ilhas vizinhas de entrada.  %
%-------------------------------------------------------------------------------------------------------------------------------%

tira_ilhas_terminadas_entrada(TITE_Ilhas_term, TITE_Entrada, TITE_Nova_entrada) :-
    TITE_Entrada = [TITE_Ilha, TITE_Vizinhas, TITE_Pontes],
    findall(X, (member(X, TITE_Vizinhas), \+member(X, TITE_Ilhas_term)), TITE_NEntrada),
    TITE_Nova_entrada = [TITE_Ilha, TITE_NEntrada, TITE_Pontes].
    

%------------------------------------------------------------------------------------------------------------------------------------%
% 2.12.tira_ilhas_terminadas(TIT_Estado, TIT_Ilhas_term, TIT_Novo_estado):                                                           %
%  -> TIT_Estado eh um estado.                                                                                                       %
%  -> TIT_Ilhas_term eh uma lista de ilhas terminadas.                                                                               %
%  -> TIT_Novo_estado eh o estado resultante de aplicar o predicado tira_ilhas_terminadas_entrada a cada uma das entradas de Estado. %
%------------------------------------------------------------------------------------------------------------------------------------%

tira_ilhas_terminadas(TIT_Estado, TIT_Ilhas_term, TIT_Novo_estado) :-
    maplist(tira_ilhas_terminadas_entrada(TIT_Ilhas_term), TIT_Estado, TIT_Novo_estado).
    

%--------------------------------------------------------------------------------------------------------------------------------------%
% 2.13.marca_ilhas_terminadas_entrada(MITE_Ilhas_term, MITE_Entrada, MITE_Nova_entrada):                                               %
%  -> MITE_Ilhas_term eh uma lista de ilhas terminadas.                                                                                %
%  -> MITE_Entrada eh uma entrada.                                                                                                     %
%  -> MITE_Nova_entrada eh a entrada obtida de MITE_Entrada da seguinte forma: se a ilha de MITE_Entrada pertencer a MITE_Ilhas_term,  %
%     o numero de pontes desta eh substituido por 'X', em caso contrario MITE_Nova_entrada eh igual a MITE_Entrada.                     % 
%--------------------------------------------------------------------------------------------------------------------------------------%

marca_ilhas_terminadas_entrada(MITE_Ilhas_term, MITE_Entrada, MITE_Nova_entrada) :-
    MITE_Entrada = [MITE_Ilha, MITE_Vizinhas, MITE_Pontes],
    (member(MITE_Ilha, MITE_Ilhas_term) ->
    MITE_Ilha = ilha(_, MITE_Coordenadas),
    MITE_Nova_entrada = [ilha('X', MITE_Coordenadas), MITE_Vizinhas, MITE_Pontes];
    MITE_Nova_entrada = [MITE_Ilha, MITE_Vizinhas, MITE_Pontes]).


%------------------------------------------------------------------------------------------------------------------------------------------%
% 2.14.marca_ilhas_terminadas(MIT_Estado, MIT_Ilhas_term, MIT_Novo_estado):                                                                %
%  -> MIT_Estado eh um estado.                                                                                                             %
%  -> MIT_Ilhas_term eh uma lista de ilhas terminadas.                                                                                     %
%  -> MIT_Novo_estado eh o estado resultante de aplicar o predicado marca_ilhas_terminadas_entrada a cada uma das entradas de MIT_Estado.  %
%------------------------------------------------------------------------------------------------------------------------------------------%

marca_ilhas_terminadas(MIT_Estado, MIT_Ilhas_term, MIT_Novo_estado) :-
    maplist(marca_ilhas_terminadas_entrada(MIT_Ilhas_term), MIT_Estado, MIT_Novo_estado).


%-----------------------------------------------------------------------------------------------------------------------------------%
% 2.15.trata_ilhas_terminadas(TIT_Estado, TIT_Novo_estado):                                                                         %
%  -> TIT_Estado eh um estado.                                                                                                      %
%  -> TIT_Novo_estado eh o estado resultante de aplicar os predicados tira_ilhas_terminadas e marca_ilhas_terminadas a TIT_Estado.  %
%-----------------------------------------------------------------------------------------------------------------------------------%

trata_ilhas_terminadas(TIT_Estado, TIT_Novo_estado) :-
    ilhas_terminadas(TIT_Estado, TIT_Ilhas_term),
    tira_ilhas_terminadas(TIT_Estado, TIT_Ilhas_term, TIT_NEstado),
    marca_ilhas_terminadas(TIT_NEstado, TIT_Ilhas_term, TIT_Novo_estado).


%--------------------------------------------------------------------------------------------------------------------------%
% 2.16.junta_pontes(JP_Estado, JP_Num_pontes, JP_Ilha1, JP_Ilha2, JP_Novo_estado):                                         %
%  -> JP_Estado eh um estado.                                                                                              %
%  -> JP_Ilha1 e JP_Ilha2 sao 2 ilhas.                                                                                     %
%  -> JP_Novo_estado eh o estado que se obtem  de JP_Estado por adicao de JP_Num_pontes pontes entre JP_Ilha1 e JP_Ilha2.  %
%                                                                                                                          %
% FUNCOES AUXILIARES:                                                                                                      %
%  -> unifica(JP_Ponte):                                                                                                   %
%      -> Funcao auxiliar para maplist(), serve para introduzir o numero de pontes pedido.                                 %
%  -> verifica_pontes(JP_Pos1, JP_Pos2, JP_TPontes, JP_Estado, JP_Goal):                                                   %
%      -> Funcao auxiliar para maplist(), verifica se a ilha atual esta ligada ah ponte atual e se tal adiciona-a na       %
%         representacao pedida pelo enunciado.                                                                             %
%--------------------------------------------------------------------------------------------------------------------------%

junta_pontes(JP_Estado, JP_Num_pontes, JP_Ilha1, JP_Ilha2, JP_Novo_estado) :-
    JP_Ilha1 = ilha(_,JP_Pos1),
    JP_Ilha2 = ilha(_,JP_Pos2),
    cria_ponte(JP_Pos1, JP_Pos2, JP_Ponte),
    length(JP_TPontes, JP_Num_pontes),
    maplist(unifica(JP_Ponte), JP_TPontes),
    maplist(verifica_pontes(JP_Pos1, JP_Pos2, JP_TPontes), JP_Estado, JP_NPontes),
    actualiza_vizinhas_apos_pontes(JP_NPontes, JP_Pos1, JP_Pos2, JP_NEstado),
    trata_ilhas_terminadas(JP_NEstado, JP_Novo_estado).

unifica(JP_Ponte, JP_Ponte).
verifica_pontes(JP_Pos1, JP_Pos2, JP_Ponte, JP_Estado, JP_Goal) :-
    JP_Estado = [JP_Ilha, JP_Vizinhas, JP_OPonte],
    append(JP_OPonte, JP_Ponte, JP_NPonte),
    JP_Ilha = ilha(_,JP_Pos),
    (memberchk(JP_Pos, [JP_Pos1, JP_Pos2]),
    JP_Goal = [JP_Ilha, JP_Vizinhas, JP_NPonte], !;
    JP_Goal = [JP_Ilha, JP_Vizinhas, JP_OPonte]).
    