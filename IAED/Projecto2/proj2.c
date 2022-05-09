/*
 * Ficheiro: proj2.c
 * Autor: vmm
 * Co-Autor: David Pires, 103458
 * Descrição: Segundo projeto de IAED 2021/2022
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "variables.h"


/* Funcoes Leitura */

Hora leHora() {
	Hora h;
	scanf("%d:%d", &h.hora, &h.minuto);
	return h;
}


Data leData() {
	Data d;
	scanf("%d-%d-%d", &d.dia, &d.mes, &d.ano);
	return d;
}


int leNumero() {
	int n;
	scanf("%d",&n);
	return n;
}


int leProximaPalavra(char str[]) {
	char c = getchar();
	int i = 0;
	while (c == ' ' || c == '\t')
		c = getchar();
	while (c != ' ' && c != '\t' && c != '\n') {
		str[i++] = c;
		c = getchar();
	}
	str[i] = '\0';
	return (c == '\n');
}


void lePalavraAteFimDeLinha(char str[]) {
	char c = getchar();
	int i = 0;
	while (c == ' ' || c == '\t')
		c = getchar();
	while (c != '\n') {
		str[i++] = c;
		c = getchar();
	}
	str[i] = '\0';
}


void leAteFimDeLinha() {
	char c = getchar();
	while (c != '\n')
		c = getchar();
}


/* Funcoes Datas e Horas */

void mostraData(Data d) {
	if (d.dia < 10)
		printf("0");
	printf("%d-", d.dia);
	if (d.mes < 10)
		printf("0");
	printf("%d-%d", d.mes, d.ano);
}


void mostraHora(Hora h) {
	if (h.hora < 10)
		printf("0");
	printf("%d:", h.hora);
	if (h.minuto < 10)
		printf("0");
	printf("%d", h.minuto);
}


int converteDataNum(Data d) {
	return (d.ano - ANO_INICIO) * DIAS_ANO + _diasMesAc[d.mes - 1] +
		d.dia - 1;
}


int converteHoraNum(Hora h) {
	return ((h.hora * MINUTOS_HORA) + h.minuto);
}


int converteDataHoraNum(Data d, Hora h) {
	return converteDataNum(d) * MINUTOS_DIA + converteHoraNum(h);
}


Hora converteNumHora(int num) {
	Hora h;
	h.minuto = num % MINUTOS_HORA;
	h.hora = ((num - h.minuto) / MINUTOS_HORA) % HORAS_DIA;
	return h;
}


Data converteNumData(int num) {
	Data d;
	int i = 0;
	num = (num - (num % MINUTOS_DIA)) / MINUTOS_DIA;
	d.ano = (num / DIAS_ANO) + ANO_INICIO;
	num = num - ((d.ano - ANO_INICIO) * DIAS_ANO);
	while (i <= 11 && num >= _diasMesAc[i])
		i++;
	d.mes = i;
	d.dia = num - _diasMesAc[i - 1] + 1;
	return d;
}


int validaData(Data d) {
	int numData = converteDataNum(d);
	Data proximoAno = _hoje;
	proximoAno.ano++;
	return !(numData < converteDataNum(_hoje)
		 || numData > converteDataNum(proximoAno));
}


int validaHora(Hora h) {
	return !(h.hora > 12 || (h.hora == 12 && h.minuto > 0));
}


/* Algoritmo de ordenação BubbleSort */

void bubbleSort(int indexes[], int size, int (*cmpFunc)(int a, int b)) {
	int i, j, done;

	for (i = 0; i < size - 1; i++) {
		done = 1;
		for (j = size - 1; j > i; j--)
			if ((*cmpFunc) (indexes[j - 1], indexes[j])) {
				int aux = indexes[j];
				indexes[j] = indexes[j - 1];
				indexes[j - 1] = aux;
				done = 0;
			}
		if (done)
			break;
	}
}


/* Funcoes Aeroportos */


int aeroportoInvalido(char id[]) {
	int i;
	for (i = 0; id[i] != '\0'; i++)
		if (!(id[i] >= 'A' && id[i] <= 'Z'))
			return TRUE;
	return FALSE;
}


int encontraAeroporto(char id[]) {
	int i;
	for (i = 0; i < _numAeroportos; i++)
		if (!strcmp(id, _aeroportos[i].id))
			return i;
	return NAO_EXISTE;
}


void adicionaAeroporto() {
	Aeroporto a;

	leProximaPalavra(a.id);
	leProximaPalavra(a.pais);
	lePalavraAteFimDeLinha(a.cidade);

	if (aeroportoInvalido(a.id))
		printf(ERR_INVALID_AIRPORT);
	else if (_numAeroportos == MAX_NUM_AEROPORTOS)
		printf(ERR_TOO_MANY_AIRPORTS);
	else if (encontraAeroporto(a.id) != NAO_EXISTE)
		printf(ERR_DUPLICATED_AIRPORT);
	else {
		strcpy(_aeroportos[_numAeroportos].id, a.id);
		strcpy(_aeroportos[_numAeroportos].pais, a.pais);
		strcpy(_aeroportos[_numAeroportos].cidade, a.cidade);
		_aeroportos[_numAeroportos].numVoos = 0;
		_numAeroportos++;
		printf("airport %s\n", a.id);
	}
}


void mostraAeroporto(int index) {
	printf("%s %s %s %d\n", _aeroportos[index].id,
		_aeroportos[index].cidade, _aeroportos[index].pais,
		_aeroportos[index].numVoos);
}


int cmpAeroportos(int a, int b) {
	return (strcmp(_aeroportos[a].id, _aeroportos[b].id) > 0);
}


void listaTodosAeroportos() {
	int i;
	int indexAeroportos[MAX_NUM_AEROPORTOS];

	for (i = 0; i < _numAeroportos; i++)
		indexAeroportos[i] = i;

	bubbleSort(indexAeroportos, _numAeroportos, cmpAeroportos);

	for (i = 0; i < _numAeroportos; i++)
		mostraAeroporto(indexAeroportos[i]);
}


void listaAeroportos() {
	char id[MAX_CODIGO_AEROPORTO];
	int indexAeroporto, ultima = 0;

	ultima = leProximaPalavra(id);
	if (strlen(id) == 0)
		listaTodosAeroportos();
	else {
		while (strlen(id) != 0) {
			indexAeroporto = encontraAeroporto(id);
			if (indexAeroporto == NAO_EXISTE)
				printf("%s: %s", id, ERR_NO_SUCH_AIRPORT);
			else
				mostraAeroporto(indexAeroporto);
			if (!ultima)
				ultima = leProximaPalavra(id);
			else
				break;
		}
	}
}



/* Funcoes Voos */

void mostraVoo(int index) {
	printf("%s %s %s ", _voos[index].id, _voos[index].partida,
		_voos[index].chegada);
	mostraData(_voos[index].data);
	printf(" ");
	mostraHora(_voos[index].hora);
	printf("\n");
}

void mostraVooPartida(int index) {
	printf("%s %s ", _voos[index].id, _voos[index].chegada);
	mostraData(_voos[index].data);
	printf(" ");
	mostraHora(_voos[index].hora);
	printf("\n");
}

void mostraVooChegada(int index) {
	Hora h = converteNumHora(_voos[index].horaChegada);
	printf("%s %s ", _voos[index].id, _voos[index].partida);
	mostraData(converteNumData(_voos[index].horaChegada));
	printf(" ");
	mostraHora(h);
	printf("\n");
}



int encontraVoo(char id[], Data d) {
	int numData = converteDataNum(d);
	int i;

	for (i = 0; i < _numVoos; i++)
		if (!strcmp(id, _voos[i].id)
			&& numData == converteDataNum(_voos[i].data))
			return i;
	return NAO_EXISTE;
}


int validaIDVoo(char id[]) {
	int i = 0, l = strlen(id);
	if (l < 3)
		return FALSE;
	for (i = 0; i < 2; i++)
		if (!(id[i] >= 'A' && id[i] <= 'Z'))
			return FALSE;

	while (id[i] != '\0') {
		if (!(id[i] >= '0' && id[i] <= '9'))
			return FALSE;
		i++;
	}
	return TRUE;
}

int validaVoo(Voo v) {
	if (validaIDVoo(v.id) == FALSE)
		printf(ERR_INVALID_FLIGHT);
	else if (encontraVoo(v.id, v.data) != NAO_EXISTE)
		printf(ERR_FLIGHT_ALREADY_EXISTS);
	else if (encontraAeroporto(v.partida) == NAO_EXISTE)
		printf("%s: %s", v.partida, ERR_NO_SUCH_AIRPORT);
	else if (encontraAeroporto(v.chegada) == NAO_EXISTE)
		printf("%s: %s", v.chegada, ERR_NO_SUCH_AIRPORT);
	else if (_numVoos == MAX_NUM_VOOS)
		printf(ERR_TOO_MANY_FLIGHTS);
	else if (validaData(v.data) == FALSE)
		printf(ERR_INVALID_DATE);
	else if (validaHora(v.duracao) == FALSE)
		printf(ERR_INVALID_DURATION);
	else if (v.capacidade < 10)
		printf(ERR_INVALID_CAPACITY);
	else
		return TRUE;
	return FALSE;
}

void criaVoo(Voo v) {
	strcpy(_voos[_numVoos].id, v.id);
	strcpy(_voos[_numVoos].partida, v.partida);
	strcpy(_voos[_numVoos].chegada, v.chegada);
	_voos[_numVoos].data = v.data;
	_voos[_numVoos].hora = v.hora;
	_voos[_numVoos].duracao = v.duracao;
	_voos[_numVoos].capacidade = v.capacidade;
	_voos[_numVoos].horaPartida =
		converteDataHoraNum(_voos[_numVoos].data,
					_voos[_numVoos].hora);
	_voos[_numVoos].horaChegada =
		_voos[_numVoos].horaPartida +
		converteHoraNum(_voos[_numVoos].duracao);
	_aeroportos[encontraAeroporto(v.partida)].numVoos++;
	_voos[_numVoos].totReservas = 0;
	_voos[_numVoos].reservas = NULL;
	_numVoos++;
}

void adicionaListaVoos() {
	Voo v;
	int i;

	if (leProximaPalavra(v.id)) {
		for (i = 0; i < _numVoos; i++)
			mostraVoo(i);
		return;
	} else {
		leProximaPalavra(v.partida);
		leProximaPalavra(v.chegada);
		v.data = leData();
		v.hora = leHora();
		v.duracao = leHora();
		scanf("%d", &v.capacidade);
		leAteFimDeLinha();
	}

	if (validaVoo(v))
		criaVoo(v);
}


int cmpVoosPartida(int a, int b) {
	return (_voos[a].horaPartida > _voos[b].horaPartida);
}


int cmpVoosChegada(int a, int b) {
	return (_voos[a].horaChegada > _voos[b].horaChegada);
}


void listaVoosPartida() {
	int indexVoos[MAX_NUM_VOOS], i, n = 0;
	char partida[MAX_CODIGO_AEROPORTO];

	lePalavraAteFimDeLinha(partida);

	if (encontraAeroporto(partida) == NAO_EXISTE)
		printf("%s: %s", partida, ERR_NO_SUCH_AIRPORT);

	else {
		for (i = 0; i < _numVoos; i++) {
			if (!strcmp(_voos[i].partida, partida))
				indexVoos[n++] = i;
		}

		bubbleSort(indexVoos, n, cmpVoosPartida);

		for (i = 0; i < n; i++)
			mostraVooPartida(indexVoos[i]);
	}
}


void listaVoosChegada() {
	int indexVoos[MAX_NUM_VOOS], i, n = 0;
	char chegada[MAX_CODIGO_AEROPORTO];

	lePalavraAteFimDeLinha(chegada);

	if (encontraAeroporto(chegada) == NAO_EXISTE)
		printf("%s: %s", chegada, ERR_NO_SUCH_AIRPORT);

	else {
		for (i = 0; i < _numVoos; i++) {
			if (!strcmp(_voos[i].chegada, chegada))
				indexVoos[n++] = i;
		}

		bubbleSort(indexVoos, n, cmpVoosChegada);

		for (i = 0; i < n; i++)
			mostraVooChegada(indexVoos[i]);
	}
}


void alteraData() {
	Data d;

	d = leData();
	leAteFimDeLinha();
	if (validaData(d) == FALSE)
		printf(ERR_INVALID_DATE);
	else {
		_hoje = d;
		mostraData(_hoje);
		printf("\n");
	}
}


/*********************/

/* Funcoes projeto 2 */

/*********************/


void eliminaReservas (int i) {
	if (_voos[i].reservas != NULL) {
		while (_voos[i].reservas != NULL) {
			Reserva *temp = _voos[i].reservas;

			free(temp->reserva);
			_voos[i].reservas = temp->prox;
			free(temp);
		}
	}
}


void limpaMemoria() {
	int i;

	for (i=0; i<_numVoos; i++) {
		eliminaReservas(i);
	}
}


void* criaMalloc(int i) {
	if (malloc(i)==NULL) {
		printf(ERR_NO_MEMORY);
		limpaMemoria();
		exit(0);
	}
	return malloc(i);
}


void criaReserva(char reserva[], int passageiros, int voo) {
	Reserva *x = malloc(sizeof(Reserva));

	x->reserva = malloc((strlen(reserva)+1)*sizeof(char));
	x->passageiros = passageiros;
	strcpy(x->reserva, reserva);

	/* primeiro elemento */
	if (_voos[voo].reservas==NULL) x->prox = NULL, _voos[voo].reservas = x;

	/* inserir no inicio */
	if (strcmp(x->reserva, _voos[voo].reservas->reserva)<0) {
		x->prox = _voos[voo].reservas;
		_voos[voo].reservas = x;
	}
	/* inserir a meio ou fim */
	else {
		Reserva *temp = _voos[voo].reservas;
		int s=0;

		while (temp->prox != NULL) {
			/* inserir a meio */
			if (strcmp(x->reserva, temp->prox->reserva)<0){
				x->prox = temp->prox;
				temp->prox = x;
				s++;
				break;
			}
			temp = temp->prox;
		}
		/* inserir no fim */
		if (s==0) temp->prox = x, x->prox = NULL;
	}
}



int reservaInvalida(char reserva[]) {
	int i, l;

	l = strlen(reserva);
	if (l<10) return TRUE;

	for (i=0; i<l; i++) {
		if (!isdigit(reserva[i]) && !isupper(reserva[i])) {
			return TRUE;
		}
	}

	return FALSE;
}


void adicionaReserva(char reserva[], int passageiros, int voo) {
	int p = _voos[voo].totReservas+=passageiros;
	int s=0, i=0;

	if (p>_voos[voo].capacidade) {
		_voos[voo].totReservas-=passageiros;
		printf(ERR_TOO_MANY_RESERVATIONS);
		s++;
	}

	for (i=0; i<_numVoos; i++) {
		Reserva *temp = _voos[i].reservas;

		/* temp = NULL, nao existem reservas */
		while (temp != NULL) {
			if (!strcmp(temp->reserva, reserva)) {
				printf("%s: %s", reserva, ERR_RES_ALREADY_EXISTS);
				s++;
				break;
			}
			temp = temp->prox;
		}
	}

	if (s==0) {
		criaReserva(reserva, passageiros, voo);
	}
}


void listaReservas(int voo) {
	Reserva *temp = _voos[voo].reservas;

	while (temp!=NULL) {
		printf("%s %d\n", temp->reserva, temp->passageiros);
		temp = temp->prox;
	}
}


int verificaReserva(char reserva[], int passageiros) {

	/* flight reservation already used */
	if (reservaInvalida(reserva)) {
		printf(ERR_INVALID_RESERVATION);
		return FALSE;
	}
	else if (passageiros<1) {
		printf(ERR_INVALID_PASSANGER_NUM);
		return FALSE;
	}

	return TRUE;
}


void adicionaListaReservas() {
	char codigo[MAX_CODIGO_VOO], input[BUFFER_SIZE], *reserva;
	int passageiros, voo;
	Data data;

	leProximaPalavra(codigo);
	data = leData();
	voo = encontraVoo(codigo, data);

	if (voo==NAO_EXISTE) printf("%s: %s", codigo, ERR_FLIGHT_DOES_NOT_EXISTS);
	else if (validaData(data) == FALSE) printf(ERR_INVALID_DATE);

	else if (!leProximaPalavra(input)) {
		passageiros = leNumero();

		reserva = malloc((strlen(input)+1)*sizeof(char));
		strcpy(reserva,input);

		if (verificaReserva(reserva, passageiros)) {
			adicionaReserva(reserva, passageiros, voo);
		}
		free(reserva);
	}
	else {
		listaReservas(voo);
	}
}


void eliminaVoo(char id[]) {
	int i=0, d=0, e=0, j=0;
	Voo *v=_voos;

	for (i = 0; i < _numVoos; i++) {
		d=0;
		if (!strcmp(id, v->id)) {
			d++, e++;
			eliminaReservas(i-d);
			for (j=0; j<_numVoos; j++) {memcpy(v[j].id,v[j+d].id,sizeof(Voo));}
		}
		v+=(1-d);
	}
	_numVoos -= e;
	if (e==0) printf(ERR_NOT_FOUND);
}


void eliminaReserva(char id[]) {
	int i=0, e=0, p=0;

	for (i=0; i<_numVoos; i++) {
		if (_voos[i].reservas != NULL) {
			Reserva *temp = _voos[i].reservas;
			Reserva *ttemp = _voos[i].reservas;

			/* elimina primeiro elemento */
			if (!strcmp(temp->reserva,id)) {
				_voos[i].reservas = temp->prox, p = temp->passageiros;
				free(temp->reserva), free(temp), e++;
			}

			/* elimina elementos no meio ou fim */
			else {
				while (temp != NULL) {
					if (!strcmp(temp->reserva,id)) {
						ttemp->prox = temp->prox, p = temp->passageiros;
						free(temp->reserva), free(temp), e++;
					}
					ttemp = temp, temp = temp->prox;
				}
			}
			if (e!=0) {_voos[i].totReservas-=p; break;}
		}
	}
	if (e==0) printf(ERR_NOT_FOUND);
}


void elimina() {
	char input[BUFFER_SIZE], *codigo;
	int ultima;

	ultima = leProximaPalavra(input);
	while (strlen(input)!=0) {
		codigo = malloc((strlen(input)+1)*sizeof(char));
		strcpy(codigo,input);
		if (validaIDVoo(codigo)){
			eliminaVoo(codigo);
		}
		/* nao eh voo nem reserva */
		else if (reservaInvalida(codigo)) {
			printf(ERR_NOT_FOUND);
		}
		else {
			eliminaReserva(codigo);
		}
		free(codigo);
		if (!ultima) {
			ultima = leProximaPalavra(input);
		}
		else {
			break;
		}
	}
}


int main() {
	int c;

	while ((c = getchar()) != EOF) {
		switch (c) {
		case 'a': adicionaAeroporto();
			break;
		case 'l': listaAeroportos();
			break;
		case 'v': adicionaListaVoos();
			break;
		case 'p': listaVoosPartida();
			break;
		case 'c': listaVoosChegada();
			break;
		case 't': alteraData();
			break;
		case 'r': adicionaListaReservas();
			break;
		case 'e': elimina();
			break;
		case 'q': limpaMemoria(); return 0;
		}
	}
	return 0;
}