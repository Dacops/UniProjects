/*
 * File:        proj1.c
 * Author:      David Pires, 103458
 * Description: 1st IAED project 2021/2022
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "variables.h"

/*this file respects lizard's constraints and max column in #80.    */
/*variables.h saves several defines and global variables/vectors.   */

/*'a' function*/

/*'invalid airport ID' error check.*/
int invalid_airport(char id[]){
    int i=0;
    for (i=0; i<=(int)strlen(id); i++){
        if (islower(id[i])){
            printf(ERR_INVALID_AIRPORT);
            return 1;
        }
    }
    return 0;
}
/*'too many airports' error check.*/
int too_many_airports(int air){
    if (air==airs_num-1){
        printf(ERR_TOO_MANY_AIRPORTS);
        return 1;
    }
    return 0;
}
/*'duplicate airport' error check.*/
int duplicate_airport(char id[]){
    int i=0;
    for (i=0; i<airs_num; i++){
        if (!strcmp(id, airport[i][0])){
            printf(ERR_DUPLICATED_AIRPORT);
            return 1;
        }
        if (airport[i][0][0]=='\0'){
            break;
        }
    }
    return 0;
}
/*adds new airports*/
int a(char id[], char country[], char city[],
      char airport[][airs_arg][airs_sav], int air){

    if (invalid_airport(id))    return 0;
    if (too_many_airports(air)) return 0;
    if (duplicate_airport(id))  return 0;

    strcpy(airport[air][0], id);
    strcpy(airport[air][1], country);
    strcpy(airport[air][2], city);
    printf("airport %s\n",id);
    return 1;
}



/*'l' function*/

/*counts airports for lsearch() and lalpha()*/
int count(char entry[], char flights[][flgt_arg][flgt_sav],int fli){
    int count=0, i=0;
    for (i=0; i<fli; i++){
        if (!strcmp(entry,flights[i][1])){
            count++;
        }
    }

    return count;
}
/*lists the inputted airports*/
void lsearch(char arg[],char airport[][airs_arg][airs_sav],
             char flights[][flgt_arg][flgt_sav],int fli){
    int lin=0;      /*checks whether the airport exists.    */
    int i=0;
    /*loops all airports*/
    for (i=0; airport[i][0][0]!='\0'; i++){
        if (!strcmp(arg,airport[i][0])){
            printf("%s %s %s %d\n",airport[i][0],airport[i][2],airport[i][1],
                                    count(airport[i][0],flights,fli));
            lin++;
        }
    }
    if (lin==0){
        printf("%s: %s",arg,ERR_NO_SUCH_AIRPORT);
    }
}
/*lists the airports, alphabetically*/
void lalpha(char airport[][airs_arg][airs_sav],
            char flights[][flgt_arg][flgt_sav],int fli,int air){
    char sorted[airs_num];      /*creates an vector with the IDs sorted.    */
    int l1=10000,l2=100,l3=1;   /*variables used in the sorting algorithm.  */
    int min=1000000;            /*saves the smallest value.                 */
    int last=0;                 /*saves the last smallest value.            */
    int lindex=0;               /*saves index of smallest value.            */
    int cval=0;                 /*saves current ID value.                   */
    int i=0, j=0;
    /*Sorting algorithm, ends in a vector with sorted indexs, O(n^2).*/
    for (j=0; j<air; j++){
        min=1000000;
        for (i=0; i<air; i++){
            cval=airport[i][0][0]*l1+airport[i][0][1]*l2+airport[i][0][2]*l3;
            if (cval<min && cval>last){
                min=cval, lindex=i;
            }
        }
        last=min, sorted[j]=lindex;
    }
    /*Reads the vector produced by the algorithm*/
    for (i=0; i<air; i++){
        j=sorted[i];
        printf("%s %s %s %d\n",airport[j][0],airport[j][2],airport[j][1],
                                count(airport[j][0],flights,fli));
    }
}



/*'t' function*/
/*'t' is up here because it's used in other functions.*/
/*adds/updates date, 't' is used in 'v' error check, needs to be above it.*/
int t(char date[], char args[]){
    char *nyear, *nmonth, *nday;
    char *oyear, *omonth, *oday;
    int nval=0, oval=0;
    char nargs[date_len], ndate[date_len];

    if ((int)strlen(date)!=0){
        strcpy(nargs, args), strcpy(ndate, date);
        nday    = strtok(nargs,"-");
        nmonth  = strtok(NULL,"-");
        nyear   = strtok(NULL,"\n");
        oday    = strtok(ndate,"-");
        omonth  = strtok(NULL,"-");
        oyear   = strtok(NULL,"\n");

        /*creates UNIX like values to compare dates*/
        nval    = atoi(nyear)*372+
                  atoi(nmonth)*31+
                  atoi(nday);
        oval    = atoi(oyear)*372+
                  atoi(omonth)*31+
                  atoi(oday);
        if (nval>oval+372 || nval<oval) return 1;
    }
    return 0;
}



/*'v' function*/

/*'invalid flight code' error check.*/
int invalid_flight_code(char code[]){
    int i=0;
    for (i=0; code[i]!='\0'; i++){
        if ((i<2 && !isupper(code[i]))  ||
            (i==2 && code[i]=='0')      ||
            (i>=2 && !isdigit(code[i])) ||
            (i>5)){
            printf(ERR_INVALID_FLIGHT);
            return 1;
        }
    }
    if ((int)strlen(code)<3){
        printf(ERR_INVALID_FLIGHT);
        return 1;
    }
    return 0;
}
/*'flight already exists' error check.*/
int flight_already_exists(char flights[][flgt_arg][flgt_sav],
                          char code[], char date[]){
    int i=0;
    for(i=0; flights[i][0][0]!='\0'; i++){
        if (!strcmp(code, flights[i][0]) &&
            !strcmp(date, flights[i][3])){
            printf(ERR_FLIGHT_ALREADY_EXISTS);
            return 1;
        }
    }
    return 0;
}
/*'no such airport ID' error check.*/
int no_such_airport(char airport[][airs_arg][airs_sav],
                    char depID[], char lanID[]){
    int i=0, inl=0, ind=0;
    for (i=0; airport[i][0][0]!='\0'; i++){
        if (!strcmp(depID, airport[i][0])) ind++;
        if (!strcmp(lanID, airport[i][0])) inl++;
    }
    if (ind!=1){
        printf("%s: %s",depID,ERR_NO_SUCH_AIRPORT);
        return 1;
        }
    if (inl!=1){
        printf("%s: %s",lanID,ERR_NO_SUCH_AIRPORT);
        return 1;
    }
    return 0;
}
/*'too many flights' error check.*/
int too_many_flights(int fli){
    if (fli==flgt_num-1){
        printf(ERR_TOO_MANY_FLIGHTS);
        return 1;
    }
    return 0;
}
/*'invalid date' error check.*/
int invalid_date(char dates[],char date[]){
    if (t(dates,date)){
        printf(ERR_INVALID_DATE);
        return 1;
    }
    return 0;
}
/*'invalid duration' error check.*/
int invalid_duration(char len[]){
    char tlen[time_len], *hour, *mins;
    strcpy(tlen,len);
    hour = strtok(tlen,":");
    mins = strtok(NULL,"\n");
    if (atoi(hour)>11 && atoi(mins)>0){
        printf(ERR_INVALID_DURATION);
        return 1;
    }
    return 0;
}
/*'invalid capacity' error check.*/
int invalid_capacity(char capt[]){
    if (atoi(capt)<10 || atoi(capt)>100){
        printf(ERR_INVALID_CAPACITY);
        return 1;
    }
    return 0;
}
/*adds new flights*/
int vadd(char args[], char airport[][airs_arg][airs_sav],
         char flights[][flgt_arg][flgt_sav], char dates[], int fli){
    char *code, *depID, *lanID, *date, *time, *len, *capt;
    code    = strtok(args," \t");
    depID   = strtok(NULL," \t");
    lanID   = strtok(NULL," \t");
    date    = strtok(NULL," \t");
    time    = strtok(NULL," \t");
    len     = strtok(NULL," \t");
    capt    = strtok(NULL,"\n");

    if (invalid_flight_code(code) || flight_already_exists(flights,code,date)||
        no_such_airport(airport,depID,lanID) || too_many_flights(fli)||
        invalid_date(dates,date) || invalid_duration(len)||
        invalid_capacity(capt)){
        return 0;
    }

    strcpy(flights[fli][0], code);
    strcpy(flights[fli][1], depID);
    strcpy(flights[fli][2], lanID);
    strcpy(flights[fli][3], date);
    strcpy(flights[fli][4], time);
    strcpy(flights[fli][5], len);
    strcpy(flights[fli][6], capt);
    return 1;
}
/*lists the flights.*/
void vsort(char flights[][flgt_arg][flgt_sav],int fli){
    int i=0;
    for (i=0; i<fli; i++){
        printf("%s %s %s %s %s\n",flights[i][0],flights[i][1],flights[i][2],
                                    flights[i][3],flights[i][4]);
    }
}



/*'p', 'c' functions*/

/*month wise date changes*/
void months(int vals[]){
    if (vals[3]<=7){
        /*months with 31days*/
        if (vals[2]>31 && vals[3]%2==1){
            vals[3]++;
            vals[2]-=31;
        }
        /*months with 30days*/
        if (vals[2]>30 && vals[3]%2==0){
            vals[3]++;
            vals[2]-=30;
        }
    }
    else{
        /*months with 31days*/
        if (vals[2]>31 && vals[3]%2==0){
            vals[3]++;
            vals[2]-=31;
        }
        /*months with 30days*/
        if (vals[2]>30 && vals[3]%2==1){
            vals[3]++;
            vals[2]-=30;
        }
    }
}
/*next hour/day/month/year landing date conversions*/
void skip(int vals[],int lmins,int lhour){
    /*vals[minute,hour,day,month,year]*/
    vals[0]=vals[0]+lmins;
    vals[1]=vals[1]+lhour;

    /*minutes, hours*/
    if (vals[0]>=mins_in_hour)      vals[1]++, vals[0]-=mins_in_hour;
    if (vals[1]>=24)                vals[2]++, vals[1]-=24;

    /*february, 28dias*/
    if (vals[2]>28 && vals[3]==2)   vals[3]++, vals[2]-=28;

    /*other months*/
    /*in another function due to lizard's cyclometric restrictions*/
    months(vals);

    /*anos*/
    if (vals[3]>12)             vals[4]++, vals[3]-=12;
}
/*transforms each date into an UNIX type value, starts 01-01-2022*/
void p_sort(int sort[][2],char flights[][flgt_arg][flgt_sav],int fnum){
    char date[date_len],time[time_len],*year,*month,*day,*hour,*mins;
    int i=0, j=0, val=0;
    for (i=0; i<fnum; i++){
        j = sort[i][0];
        val = 0;
        strcpy(date,flights[j][3]);
        strcpy(time,flights[j][4]);
        day     = strtok(date,"-");
        month   = strtok(NULL,"-");
        year    = strtok(NULL,"\n");
        hour    = strtok(time,":");
        mins    = strtok(NULL,"\n");
        val     +=  (atoi(year)-default_year)*mins_in_year+
                    atoi(month)*mins_in_month+
                    atoi(day)*mins_in_day+
                    atoi(hour)*mins_in_hour+
                    atoi(mins);
        sort[i][1]=val;
    }
}
/*Sorting algorithm, ends in a vector with sorted indexs, O(n^2).*/
void p_print(int sort[][2],char flights[][flgt_arg][flgt_sav],int fnum){
    int j=0, i=0, min=0, cval=0, last=0, index=0;
    for (j=0; j<fnum; j++){
        min=2000000;
        for (i=0; i<fnum; i++){
            cval = sort[i][1];
            if (cval<min && cval>last){
                min=cval;
                index=sort[i][0];
            }
        }
        last=min;
        printf("%s %s %s %s\n",flights[index][0],flights[index][2],
                            flights[index][3],flights[index][4]);
    }
}
/*transforms each date into an UNIX type value, starts 01-01-2022*/
void c_sort(int sort[][2],char flights[][flgt_arg][flgt_sav],
                                        int fnum,int vals[]){
    char *day,*month,*year,*hour,*mins,*nhour,*nmins;
    char time[time_len], len[time_len];
    int i=0,j=0,val=0;
    for (i=0; i<fnum; i++){
        j = sort[i][0], val = 0;
        strcpy(date,flights[j][3]);
        strcpy(time,flights[j][4]);
        strcpy(len,flights[j][5]);
        day     = strtok(date,"-"),     month   = strtok(NULL,"-");
        year    = strtok(NULL,"\n"),    hour    = strtok(time,":");
        mins    = strtok(NULL,"\n"),    nhour   = strtok(len,":");
        nmins   = strtok(NULL,"\n");

        vals[0]=atoi(mins), vals[1]=atoi(hour), vals[2]=atoi(day);
        vals[3]=atoi(month), vals[4]=atoi(year);
        skip(vals,atoi(nmins),atoi(nhour));

        val     +=  (vals[4]-default_year)*mins_in_year+
                    vals[3]*mins_in_month+vals[2]*mins_in_day+
                    vals[1]*mins_in_hour+vals[0];
        sort[i][1]=val;
    }
}
/*Sorting algorithm, ends in a vector with sorted indexs, O(n^2).*/
void c_print(int sort[][2],char flights[][flgt_arg][flgt_sav],
                                        int fnum,int vals[]){
    char *day,*month,*year,*hour,*mins,*nhour,*nmins;
    char time[time_len], len[time_len];
    int j=0, i=0, min=0, cval=0, index=0, last=0;
    for (j=0; j<fnum; j++){
        min=2000000;
        for (i=0; i<fnum; i++){
            cval = sort[i][1];
            if (cval<min && cval>last) min=cval, index=sort[i][0];
        }
        last=min;

        /*if hour increase is needed due to flight duration*/
        strcpy(time,flights[index][4]), strcpy(len,flights[index][5]);
        strcpy(date,flights[index][3]);

        day     = strtok(date,"-"),     month   = strtok(NULL,"-");
        year    = strtok(NULL,"\n"),    hour    = strtok(time,":");
        mins    = strtok(NULL,"\n"),    nhour   = strtok(len,":");
        nmins   = strtok(NULL,"\n");

        vals[0]=atoi(mins), vals[1]=atoi(hour), vals[2]=atoi(day);
        vals[3]=atoi(month), vals[4]=atoi(year);
        skip(vals,atoi(nmins),atoi(nhour));
        printf("%s %s %02d-%02d-%02d %02d:%02d\n",flights[index][0],
               flights[index][1],vals[2],vals[3],vals[4],vals[1],vals[0]);
    }
}
/*sorts the airports, prints one by one, used in 'c' and 'p' commands*/
void compare(int sort[][2],char flights[][flgt_arg][flgt_sav],int fnum,
                                                            int mode){
    int vals[date_len];

    /*works for 'p' command, else for 'c' command*/
    if (mode){
        p_sort(sort,flights,fnum);
        p_print(sort,flights,fnum);
    }
    else{
        c_sort(sort,flights,fnum,vals);
        c_print(sort,flights,fnum,vals);
    }
}
/*checks whether an airport exists, used in various functions*/
int exists(char airport[][airs_arg][airs_sav], char check[]){
    int exis=0; /*checks if x airport exists.           */
    int i=0;

    for (i=0; airport[i][0][0]!='\0'; i++){
        if (!strcmp(check,airport[i][0])){
            exis++;
        }
    }
    return exis;
}



/*These functions receives arguments and formats them for the main function.*/
void prep_a(char entry[]){
    char *id;
    char *country;
    char *city;
    (void)entry;
    id      = strtok(NULL," \t");
    country = strtok(NULL," \t");
    city    = strtok(NULL,"\n");
    if (a(id,country,city,airport,air)) air++;
}
void prep_l(char entry[]){
    (void)entry;
    args = strtok(NULL," \t");
    /*arguments inputted, list inputted airports.*/
    if (args){
        while (args){
            lsearch(args,airport,flights,fli);
            args = strtok(NULL," \t");
        }
    }
    /*no argument, lists airports.*/
    else{
        lalpha(airport,flights,fli,air);
    }
}
void prep_v(char entry[]){
    (void)entry;
    args = strtok(NULL,"\n");
    /*arguments inputted, add flight.*/
    if (args){
        if (vadd(args,airport,flights,date,fli)) fli++;
    }
    /*no argument, lists flights.*/
    else{
        vsort(flights,fli);
    }
}
void prep_p(char entry[]){
    int fnum=0; /*flight that leaves x airport index.   */
    int cflg=0; /*current flight index.                 */
    int i=0;
    (void)entry;
    args = strtok(NULL,"\n");
    for (i=0; i<fli; i++){
        if (!strcmp(args,flights[i][1])){
            sort[fnum][0]=cflg;
            fnum++;
        }
        cflg++;
    }
    if (exists(airport,args)){
        compare(sort,flights,fnum,1);
    }
    else{
        printf("%s: %s",args,ERR_NO_SUCH_AIRPORT);
    }
}
void prep_c(char entry[]){
    int fnum=0; /*flight that leaves x airport index.   */
    int cflg=0; /*current flight index.                 */
    int i=0;
    (void)entry;
    args = strtok(NULL,"\n");
    for (i=0; i<fli; i++){
        if (!strcmp(args,flights[i][2])){
            sort[fnum][0]=cflg;
            fnum++;
        }
        cflg++;
    }
    if (exists(airport,args)){
        compare(sort,flights,fnum,0);
    }
    else{
        printf("%s: %s",args,ERR_NO_SUCH_AIRPORT);
    }
}
void prep_t(char entry[]){
    (void)entry;
    args = strtok(NULL,"\n");
    if (t(date,args)){
        printf(ERR_INVALID_DATE);
    }
    else{
        strcpy(date,args);
        printf("%s\n",args);
    }
}



int main(){
    char *command;                      /*saves command.*/
    strcpy(date,DEFAULT_DATE);          /*default date. */
    while (1){
        scanf("%[^\n]", entry);         /*reads entry.  */
        getchar();                      /*reads \n.     */
        command = strtok(entry," \t");  /*gets  command.*/

        switch(*command){
            case 'a':   prep_a(entry);
                        break;
            case 'l':   prep_l(entry);
                        break;
            case 'v':   prep_v(entry);
                        break;
            case 'p':   prep_p(entry);
                        break;
            case 'c':   prep_c(entry);
                        break;
            case 't':   prep_t(entry);
                        break;
            case 'q':   return 0;
                        break;
        }
    }
}
