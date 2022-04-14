/*
 * File:        variables.h
 * Author:      David Pires, 103458
 * Description: Defines, Vectors and Variables for proj1.c
*/


/*Vector lenght defines*/
#define DIM             201                 /*dimension of the entry vector.                */
#define airs_num        41                  /*number of airports in the vector.             */
#define airs_arg        4                   /*number of arguments per airport.              */
#define airs_sav        51                  /*space to save the arguments from airport.     */
#define flgt_num        30001               /*number of flights in the vector.              */
#define flgt_arg        9                   /*number of arguments per flight.               */
#define flgt_sav        11                  /*space to save the arguments from flight.      */
#define date_len        11                  /*lenght of dates.                              */
#define time_len        6                   /*lenght of time.                               */
#define DEFAULT_DATE    "01-01-2022"        /*default date used on 't'                      */
#define mins_in_year    535680              /*minutes in a year.                            */
#define mins_in_month   44640               /*minutes in a month.                           */
#define mins_in_day     1440                /*minutes in a day.                             */
#define mins_in_hour    60                  /*minutes in a hour.                            */
#define default_year    2022                /*default year.                                 */

/*error defines*/
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


/*Global Variables, Vectors*/
char entry[DIM];                            /*creates entry vector.                         */
char airport[airs_num][airs_arg][airs_sav]; /*creates vector to save airports info.         */
                                            /*1st field: 40 airports.                       */
                                            /*2nd field: 3 args (ID, Country, City).        */
                                            /*3rd field: max arg length (City).             */
char flights[flgt_num][flgt_arg][flgt_sav]; /*creates vector to save fligths info.          */
                                            /*1st field - 30000 flights.                    */
                                            /*2nd field - 7 args (FlightCode, DepartedID,   */
                                            /*            LandingID, Date, Time, Lenght,    */
                                            /*            Capacity).                        */
                                            /*3rd field - max arg length (DepartedDate).    */
char date[date_len];                        /*vector to save current date, used in 't'.     */
int sort[flgt_num][2];                      /*creates vectors used in sorting algorithm.    */
int air=0;                                  /*saves current airport 'slot'.                 */
int fli=0;                                  /*saves current flights 'slot'.                 */
char *args;                                 /*gets args from inputted commands.             */










