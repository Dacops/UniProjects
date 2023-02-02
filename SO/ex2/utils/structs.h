#ifndef __STRUCTS_H__
#define __STRUCTS_H__

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/select.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>


#define MAX_REQUEST_SIZE 289
#define MAX_MESSAGE_SIZE 1024
#define MAX_ANSWER_SIZE 1029
#define MAX_BOX_NAME 32
#define MAX_PIPE_NAME 256
#define MAX_BUFFER_MESSAGE 1025
#define MAX_LIST_ANSWER 58

typedef struct {
    char message_box[MAX_BOX_NAME];
    int pipe_fd; //file descriptor for the name pipe
    int server_fd; // file descriptor for the register pipe
} manager_t;

typedef struct publisher_t{
    int pipe_fd; //file descriptor for the name pipe
    int server_fd; // file descriptor for the register pipe
    char message_box[MAX_BOX_NAME]; //name of the message box
    char pipe_name[MAX_PIPE_NAME]; //name of the pipe
} publisher_t;

typedef struct subscriber_t{
    int pipe_fd; //file descriptor for the name pipe
    int server_fd; // file descriptor for the register pipe
    char pipe_name[MAX_PIPE_NAME]; //name of the pipe
    char message_box[MAX_BOX_NAME]; //name of the message box
    int num_messages; //number of messages received
} subscriber_t;

typedef struct {
    void *(*thread_func)(void *);
    void *arg;
}session_t;

typedef struct node_t {
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    char box_name[MAX_BOX_NAME];
    uint64_t box_size;
    uint64_t n_pubs;
    uint64_t n_subs;
    struct node_t *next; 
}node_t;


void change_global_pipe_name(char new_name[MAX_PIPE_NAME]);

void INT_handler(int signum);

void build_request(uint8_t code, char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME], char *buffer);

void build_answer_to_list(uint8_t code, uint8_t last, char box_name[MAX_BOX_NAME], uint64_t box_size, uint64_t n_pubs, uint64_t n_subs, char *buffer);

void build_answer_to_box(uint8_t code, int32_t return_code, const char *err_message, char *buffer);

void build_message(uint8_t code, char message[MAX_MESSAGE_SIZE], char *buffer);

void add_box(node_t **head,char box_name[MAX_BOX_NAME]);

int rm_box(node_t **head ,char box_name[MAX_BOX_NAME]);

node_t *get_box(node_t **head ,char box_name[MAX_BOX_NAME]);

void add_pub(node_t **head, char box_name[MAX_BOX_NAME]);

void rm_pub(node_t **head, char box_name[MAX_BOX_NAME]);

void add_sub(node_t **head, char box_name[MAX_BOX_NAME]);

void rm_sub(node_t **head, char box_name[MAX_BOX_NAME]);

#endif