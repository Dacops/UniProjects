/*
 * Ficheiro:    variables.h
 * Autor:       David Pires, 103458
 * Descrição:   Valores, Tipos de Dados e Variáveis de proj2.c
*/


/* Valores */
#define MAX_NUM_AEROPORTOS 40       /* número máximo de areoportos      */
#define MAX_NUM_VOOS 30000          /* número máximo de voos            */
#define MAX_CODIGO_AEROPORTO 4      /* dimensão do código do aeroporto  */
#define MAX_NOME_PAIS 31            /* dimensão do nome do pais         */
#define MAX_NOME_CIDADE 51          /* dimensão do nome da cidade       */
#define MAX_CODIGO_VOO 7            /* dimensão do código do voo        */
#define MAX_DATA 11                 /* dimensão da data                 */
#define MAX_HORA 6                  /* dimensão da hora                 */
#define NAO_EXISTE -1               /* código de erro                   */
#define ANO_INICIO 2022             /* ano inicial do sistema           */
#define DIAS_ANO 365                /* número de dias no ano            */
#define HORAS_DIA 24                /* número de horas por dia          */
#define MINUTOS_HORA 60             /* número de minutos numa hora      */
#define MINUTOS_DIA 1440            /* número de minutos do dia         */
#define TRUE 1                      /* verdadeiro                       */
#define FALSE 0                     /* falso                            */
#define BUFFER_SIZE 65536			/* tamanho do buffer para proj2		*/


/* Erros */
#define ERR_NO_SUCH_AIRPORT         "no such airport ID\n"
#define ERR_INVALID_DATE            "invalid date\n"
#define ERR_INVALID_AIRPORT         "invalid airport ID\n"
#define ERR_TOO_MANY_AIRPORTS       "too many airports\n"
#define ERR_DUPLICATED_AIRPORT      "duplicate airport\n"
#define ERR_INVALID_FLIGHT          "invalid flight code\n"
#define ERR_FLIGHT_ALREADY_EXISTS   "flight already exists\n"
#define ERR_TOO_MANY_FLIGHTS        "too many flights\n"
#define ERR_INVALID_DURATION        "invalid duration\n"
#define ERR_INVALID_CAPACITY        "invalid capacity\n"
#define ERR_INVALID_RESERVATION		"invalid reservation code\n"
#define ERR_FLIGHT_DOES_NOT_EXISTS	"flight does not exist\n"
#define ERR_INVALID_PASSANGER_NUM	"invalid passenger number\n"
#define ERR_TOO_MANY_RESERVATIONS	"too many reservations\n"
#define ERR_RES_ALREADY_EXISTS		"flight reservation already used\n"
#define ERR_NOT_FOUND				"not found\n"
#define ERR_NO_MEMORY				"no memory\n"


/* Tipos de Dados */
typedef struct {
	char id[MAX_CODIGO_AEROPORTO];
	char pais[MAX_NOME_PAIS];
	char cidade[MAX_NOME_CIDADE];
	int numVoos;
} Aeroporto;

typedef struct {
	int dia;
	int mes;
	int ano;
} Data;

typedef struct {
	int hora;
	int minuto;
} Hora;

typedef struct node {
	int passageiros;
	char *reserva;
	struct node *prox;
} Reserva;

typedef struct {
	char id[MAX_CODIGO_VOO];
	char partida[MAX_CODIGO_AEROPORTO];
	char chegada[MAX_CODIGO_AEROPORTO];
	Data data;
	Hora hora;
	Hora duracao;
	int capacidade;
	int horaPartida;
	int horaChegada;
	Reserva *reservas;
	int totReservas;
} Voo;

/* Variaveis Globais */
int _numAeroportos = 0;                     /* número de aeroportos introduzidos    */
Aeroporto _aeroportos[MAX_NUM_AEROPORTOS];  /* vetor de aeroportos                  */
int _numVoos = 0;                           /* número de voos introduzidos          */
Voo _voos[MAX_NUM_VOOS];                    /* vetor de voos                        */
Data _hoje = { 1, 1, 2022 };                /* data atual do sistema                */
const int _diasMesAc[] =                    /* dias acumulados por mês              */
{ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334 };