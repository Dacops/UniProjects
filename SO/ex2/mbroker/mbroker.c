#include "logging.h"
#include "operations.h"
#include "structs.h"

#include <producer-consumer.h>

// CODES
// 1 - register publisher
// 2 - register subscriber
// 3 - create message box
// 4 - answer to creating a box
// 5- request to delete a message box
// 6 - answer to deleting a message box
// 7 - request to list all boxes
// 8 - answer to list all boxes
// 9 - message from publisher to publish
// 10 - message from subscriber to receiv

pc_queue_t queue;
char mbroker_pipe[MAX_PIPE_NAME];

pthread_mutex_t boxes_mutex = PTHREAD_MUTEX_INITIALIZER;;

// in case a exit is forced by pub / sub / etc. remove the pipe, not only when SIGNAL is received
void exit_mbroker() {
    unlink(mbroker_pipe);
    exit(1);
}

void * queue_handler() {
    void *(*thread_func)(void *);
    while(true) {
        session_t *data = (session_t *)pcq_dequeue(&queue);
        thread_func = data->thread_func;
        thread_func(data->arg);

        free(data->arg);
    }
}

node_t *head = NULL;

int send_buffer(int fd, char buffer[], size_t size) {
    ssize_t bytes_written = write(fd, buffer, size);
    if(bytes_written < 0) {
        return -1;
    }
    return (int)bytes_written;
}

void start_server(char pipe_name[MAX_PIPE_NAME], int max_sessions) {

    pcq_create(&queue, (size_t)max_sessions);

    // create the threads
    pthread_t threads[max_sessions];

    for(int i = 0; i < max_sessions; i++) {
        pthread_create(&threads[i], NULL, &queue_handler, &queue);
    }

    if(tfs_init(NULL)) {
        fprintf(stdout,"Error initializing the tfs\n");
        exit_mbroker();
    }

    strcpy(mbroker_pipe, pipe_name);
    
    // create a pipe with pipe_name
    if(mkfifo(pipe_name, 0640) == -1) {
        fprintf(stdout,"Error creating the fifo\n");
        exit_mbroker();
    }
}

//-------------------------------- Publisher Functions --------------------------------

void publish(char message_buffer[MAX_BUFFER_MESSAGE], char box_name[MAX_BOX_NAME]) {
    
    // get the message
    char message[MAX_MESSAGE_SIZE];

    // clear message
    memset(message, 0, MAX_MESSAGE_SIZE);

    // fill message
    memcpy(message, message_buffer + sizeof(uint8_t), MAX_BUFFER_MESSAGE - sizeof(uint8_t));

    char buffer[MAX_BUFFER_MESSAGE];
    build_message(10, message, buffer);

    // open the box
    int box_fd = tfs_open(box_name, TFS_O_APPEND);
    if(box_fd < 0) {
        fprintf(stdout,"Error opening the box\n");
        exit_mbroker();
    }

    ssize_t bytes_written = tfs_write(box_fd, message, MAX_MESSAGE_SIZE);
    if(bytes_written < 0) {
        fprintf(stdout,"Error writing to the box\n");
        exit_mbroker();
    }

    tfs_close(box_fd);

    pthread_mutex_lock(&boxes_mutex);    
    node_t *box_node = get_box(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    if(box_node == NULL) {
        fprintf(stdout,"Error getting the box node\n");
        exit_mbroker();
    }

    //broadcast the cond of the box
    pthread_mutex_lock(&(box_node->mutex));
    pthread_cond_broadcast(&(box_node->cond));
    pthread_mutex_unlock(&(box_node->mutex));

    box_node->box_size += (uint64_t)bytes_written;
}

void * pub_thread(void *input) {
    int pipe_fd = ((publisher_t*)input)->pipe_fd;
    char box_name[MAX_BOX_NAME];
    strcpy(box_name, ((publisher_t*)input)->message_box);
    char pipe_name[MAX_PIPE_NAME];
    strcpy(pipe_name, ((publisher_t*)input)->pipe_name);

    ssize_t bytes_read;
    char message_buffer[MAX_BUFFER_MESSAGE];

    pipe_fd = open(pipe_name, O_RDONLY);

    while(true) {
        // clear the message buffer
        memset(message_buffer, 0, MAX_BUFFER_MESSAGE);

        // read the request from the pipe
        bytes_read = read(pipe_fd, message_buffer, sizeof(message_buffer));
        if(bytes_read < 0) {
            fprintf(stdout,"Error reading from the pipe\n");
            exit_mbroker();
        }else if(bytes_read != 0)
            publish(message_buffer, box_name);
        else if(bytes_read == 0)
            break;
    }

    pthread_mutex_lock(&boxes_mutex);
    rm_pub(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    close(pipe_fd);

    return NULL;
}

void pub_req_handle(char request[MAX_REQUEST_SIZE]) {
    
    // get the pipe name
    char pipe_name[MAX_PIPE_NAME];
    // clear pipe_name
    memset(pipe_name, 0, MAX_PIPE_NAME);
    // fill pipe_name
    memcpy(pipe_name, request + sizeof(uint8_t), MAX_PIPE_NAME);

    // get the box name
    char box_name[MAX_BOX_NAME];
    // clear box_name
    memset(box_name, 0, MAX_BOX_NAME);
    // fill box_name
    memcpy(box_name, request + sizeof(uint8_t) + MAX_PIPE_NAME, MAX_BOX_NAME);

    //check if the publisher is already subscribed to the box

    pthread_mutex_lock(&boxes_mutex);
    node_t *box = get_box(&head, box_name);
    if(box == NULL) {
        //unlock
        pthread_mutex_unlock(&boxes_mutex);
        unlink(pipe_name);
        return;
    }

    if(box->n_pubs > 0) {
        pthread_mutex_unlock(&boxes_mutex);    
        unlink(pipe_name);
        return;
    }
    pthread_mutex_unlock(&boxes_mutex);

    pthread_mutex_lock(&boxes_mutex);
    add_pub(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    // create a publisher_t
    publisher_t *pub = malloc(sizeof(publisher_t));
    if(pub == NULL) {
        fprintf(stdout,"Error allocating memory for the publisher\n");
        exit_mbroker();
    }
    pub->pipe_fd = 0;
    strcpy(pub->message_box, box_name);
    strcpy(pub->pipe_name, pipe_name);

    // crete session_t with the pub_thread function and the publisher_t
    session_t *session = malloc(sizeof(session_t));
    if(session == NULL) {
        fprintf(stdout,"Error allocating memory for the session\n");
        exit_mbroker();
    }
    session->thread_func = &pub_thread;
    session->arg = (void *)pub;

    // enqueue the session_t
    pcq_enqueue(&queue, session);
}

//-------------------------------- Subscriber Functions --------------------------------

void * sub_thread(void *input) {
    int pipe_fd = ((subscriber_t*)input)->pipe_fd;
    char box_name[MAX_BOX_NAME];
    strcpy(box_name, ((subscriber_t*)input)->message_box);

    pthread_mutex_lock(&boxes_mutex);
    // get the mutex and the cond from the node_t of the box
    node_t *box_node = get_box(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    char message[MAX_MESSAGE_SIZE];
    char buffer_message[MAX_BUFFER_MESSAGE];

    if(box_node == NULL) {
        strcpy(message,"Message Box doesn't exist\n");
        build_message(11, message, buffer_message);
        if (send_buffer(pipe_fd, buffer_message, MAX_BUFFER_MESSAGE) < 0) {
            fprintf(stdout,"Error sending the message\n");
            exit_mbroker();
        }
        
        return NULL;
    }
    
    pthread_mutex_t *mutex = &(box_node->mutex);
    pthread_cond_t *cond = &(box_node->cond);


    // read the messages in the box using tfs_read and create the bufer to store that message
    int box_fd = tfs_open(box_name, TFS_O_APPEND);
    if(box_fd < 0) {
        fprintf(stdout,"Error opening the box\n");
        exit_mbroker();
    }

    tfs_rewind(box_fd);
    ssize_t bytes_read = tfs_read(box_fd, &message, sizeof(message));
    if(bytes_read < 0) {
        fprintf(stdout,"Error reading from the box\n");
        exit_mbroker();
    }

    while(bytes_read != 0) {

        // if the message is complete send it to the subscriber
        build_message(10, message, buffer_message);
        if(send_buffer(pipe_fd, buffer_message, MAX_BUFFER_MESSAGE) < 0) {
            fprintf(stdout,"Error sending the message to the subscriber\n");
            exit_mbroker();
        }
        memset(buffer_message, 0, MAX_BUFFER_MESSAGE);
        memset(message, 0, MAX_MESSAGE_SIZE);

        bytes_read = tfs_read(box_fd, &message, sizeof(message));
        if(bytes_read < 0) {
            fprintf(stdout,"Error reading from the box\n");
            exit_mbroker();
        }
    }

    while(true) {
        pthread_mutex_lock(mutex);
        pthread_cond_wait(cond, mutex);
        pthread_mutex_unlock(mutex);

        bytes_read = tfs_read(box_fd, &message, sizeof(message));
        if(bytes_read < 0) {
            fprintf(stdout,"Error reading from the box\n");
            exit_mbroker();
        }

        // if the message is complete send it to the subscriber
        build_message(10, message, buffer_message);
        int written_bytes = send_buffer(pipe_fd, buffer_message, MAX_BUFFER_MESSAGE);
        if(written_bytes <= 0) {
            break;
        }
        memset(buffer_message, 0, MAX_BUFFER_MESSAGE);
        memset(message, 0, MAX_MESSAGE_SIZE);
    }

    tfs_close(box_fd);

    pthread_mutex_lock(&boxes_mutex);
    rm_sub(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    close(pipe_fd);

    return NULL;
}


void sub_req_handle(char request[MAX_REQUEST_SIZE]) {
    
    // get the pipe name
    char pipe_name[MAX_PIPE_NAME];
    // clear pipe_name
    memset(pipe_name, 0, MAX_PIPE_NAME);
    // fill pipe_name
    memcpy(pipe_name, request + sizeof(uint8_t), MAX_PIPE_NAME);

    // get the box name
    char box_name[MAX_BOX_NAME];
    // clear box_name
    memset(box_name, 0, MAX_BOX_NAME);
    // fill box_name
    memcpy(box_name, request + sizeof(uint8_t) + MAX_PIPE_NAME, MAX_BOX_NAME);

    // open the pipe
    int pipe_fd = open(pipe_name, O_WRONLY);
    if(pipe_fd < 0) {
        fprintf(stdout,"Error opening named pipe for writing\n");
        exit_mbroker();
    }

    pthread_mutex_lock(&boxes_mutex);
    // add the subscriber to the box
    add_sub(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    // create a subscriber_t
    subscriber_t *sub = malloc(sizeof(subscriber_t));
    if(sub == NULL) {
        fprintf(stdout,"Error allocating memory for the subscriber\n");
        exit_mbroker();
    }
    sub->pipe_fd = pipe_fd;
    strcpy(sub->message_box, box_name);
    
    // create session_t with the sub_thread function and the subscriber_t
    session_t *session = malloc(sizeof(session_t));
    if(session == NULL) {
        fprintf(stdout,"Error allocating memory for the session\n");
        exit_mbroker();
    }
    session->thread_func = &sub_thread;
    session->arg = (void *)sub;

    // enqueue the session_t
    pcq_enqueue(&queue, session);
}

//-------------------------------- Manager Functions --------------------------------

void * create_box(void *input) {
    int pipe_fd = ((manager_t*)input)->pipe_fd;
    char box_name[MAX_BOX_NAME];
    strcpy(box_name, ((manager_t*)input)->message_box);

    // check if box already exists in tfs
    int box_fd = tfs_open(box_name, TFS_O_APPEND);
    if(box_fd >= 0) {
        // send answer to client
        char answer[MAX_ANSWER_SIZE];
        build_answer_to_box(4, -1, "Box already exists", answer);
        if(send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            close(box_fd);
            exit_mbroker();
        }
        close(box_fd);
        return NULL;
    }
    close(box_fd);

    box_fd = tfs_open(box_name, TFS_O_CREAT);
    tfs_close(box_fd);

    if(box_fd < 0) {
        // send answer to client
        char answer[MAX_ANSWER_SIZE];
        build_answer_to_box(4, -1, "Error creating the box", answer);
        if(send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            exit_mbroker();
        }
    }

    pthread_mutex_lock(&boxes_mutex);
    // add the box to the list
    add_box(&head, box_name);
    pthread_mutex_unlock(&boxes_mutex);

    char answer[MAX_ANSWER_SIZE];
    build_answer_to_box(4, 0, "\0", answer);
    send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE);

    return NULL;
}

void create_handle(char request[MAX_REQUEST_SIZE]) {

    // get the box/pipe name
    char box_name[MAX_BOX_NAME];
    char pipe_name[MAX_PIPE_NAME];
    // clear box/pipe name
    memset(box_name, 0, MAX_BOX_NAME);
    memset(pipe_name, 0, MAX_PIPE_NAME);
    // fill box/pipe name
    memcpy(pipe_name, request + sizeof(uint8_t), MAX_PIPE_NAME);
    memcpy(box_name, request + sizeof(uint8_t) + MAX_PIPE_NAME, MAX_BOX_NAME);

    // open the pipe if its not open already
    int pipe_fd = open(pipe_name, O_WRONLY);
    if(pipe_fd < 0) {
        fprintf(stdout,"Error opening named pipe for writing\n");
        exit_mbroker();
    }

    // create a subscriber_t
    manager_t *man = malloc(sizeof(manager_t));
    if(man == NULL) {
        fprintf(stdout,"Error allocating memory for the manager\n");
        exit_mbroker();
    }
    man->pipe_fd = pipe_fd;
    strcpy(man->message_box, box_name);
    
    // create session_t with the sub_thread function and the subscriber_t
    session_t *session = malloc(sizeof(session_t));
    if(session == NULL) {
        fprintf(stdout,"Error allocating memory for the session\n");
        exit_mbroker();
    }
    session->thread_func = &create_box;
    session->arg = (void *)man;

    // enqueue the session_t
    pcq_enqueue(&queue, session);

}

void * remove_box(void *input) {
    
    // get the request, box/pipe name
    char request[MAX_REQUEST_SIZE];
    char box_name[MAX_BOX_NAME];
    char pipe_name[MAX_PIPE_NAME];
    // clear request, box/pipe name
    memset(request, 0, MAX_REQUEST_SIZE);
    memset(box_name, 0, MAX_BOX_NAME);
    memset(pipe_name, 0, MAX_PIPE_NAME);
    // fill request, box/pipe name
    memcpy(request, input, MAX_REQUEST_SIZE);
    memcpy(pipe_name, request + sizeof(uint8_t), MAX_PIPE_NAME);
    memcpy(box_name, request + sizeof(uint8_t) + MAX_PIPE_NAME, MAX_BOX_NAME);

    // open the pipe if its not open already
    int pipe_fd = open(pipe_name, O_WRONLY);
    if(pipe_fd < 0) {
        fprintf(stdout,"Error opening named pipe for writing\n");
        exit_mbroker();
    }
    
    int32_t return_code;

    // remove the box
    int ret = tfs_unlink(box_name);
    if(ret < 0) {
        // send answer to client
        char answer[MAX_ANSWER_SIZE];
        return_code = (int32_t)-1;
        build_answer_to_box(6, return_code, "Error box is open or doesnt exist.", answer);
        if(send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            exit_mbroker();
        }
        return NULL;
    }

    pthread_mutex_lock(&boxes_mutex);
    // remove the box from the list
    if(rm_box(&head, box_name) < 0) {
        pthread_mutex_unlock(&boxes_mutex);
        // send answer to client
        char answer[MAX_ANSWER_SIZE];
        return_code = (int32_t)-1;
        build_answer_to_box(6, return_code, "Error box is open or doesnt exist.", answer);
        if(send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            exit_mbroker();
        }

        return NULL;
    }
    pthread_mutex_unlock(&boxes_mutex);

    char answer[MAX_ANSWER_SIZE];
    build_answer_to_box(6, 0, "\0", answer);
    send_buffer(pipe_fd, answer, MAX_ANSWER_SIZE);

    return NULL;
}

void * list_boxes(void *input) {

    // get the request, pipe name
    char request[MAX_REQUEST_SIZE];
    char pipe_name[MAX_PIPE_NAME];
    // clear request, pipe name
    memset(request, 0, MAX_REQUEST_SIZE);
    memset(pipe_name, 0, MAX_PIPE_NAME);
    // fill request, pipe name
    strcpy(request, (char *)input);
    memcpy(pipe_name, request + sizeof(uint8_t), MAX_PIPE_NAME);

    // open the pipe if its not open already
    int pipe_fd = open(pipe_name, O_WRONLY);
    if(pipe_fd < 0) {
        fprintf(stdout,"Error opening named pipe for writing\n");
        exit_mbroker();
    }

    node_t *current = head;

    char answer[MAX_LIST_ANSWER];
    char box_name[MAX_BOX_NAME];

    if(current == NULL) {
        memset(box_name, 0, MAX_BOX_NAME);
        build_answer_to_list(8, 1, box_name, 0, 
                0, 0, answer);
        if(send_buffer(pipe_fd, answer, MAX_LIST_ANSWER) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            exit_mbroker();
        }
        return NULL;
    }

    while(current != NULL) {
        if(current->next == NULL) {
            build_answer_to_list(8, 1, current->box_name, current->box_size, 
                current->n_pubs, current->n_subs, answer);
        }else {
            build_answer_to_list(8, 0, current->box_name, current->box_size, 
                current->n_pubs, current->n_subs, answer);
        }

        if(send_buffer(pipe_fd, answer, MAX_LIST_ANSWER) == -1) {
            fprintf(stdout,"Error sending answer to client\n");
            exit_mbroker();
        }

        // clear answer buffer
        memset(answer, 0, MAX_LIST_ANSWER);

        current = current->next;

    }

    return NULL;
}


void treat_request(char request[MAX_REQUEST_SIZE]) {
    // get the code of the request to chose next behaviour
    uint8_t code;
    memset(&code, 0, sizeof(uint8_t));
    memcpy(&code, request, sizeof(uint8_t));

    char *arg = malloc(MAX_REQUEST_SIZE);
    memset(arg, 0, MAX_REQUEST_SIZE);
    memcpy(arg, request, MAX_REQUEST_SIZE);

    // create a session for the client where the arg is the request
    session_t *session = (session_t *)malloc(sizeof(session_t));
    session->arg = (void *)arg;

    switch(code) {
        default:
            break;
        case 1:
            // register publisher
            pub_req_handle(request);
            break;
        case 2:
            // register subscriber
            sub_req_handle(request);
            break;
        case 3:
            create_handle(request);
            break;
        case 5:
            // request to delete a message box
            session->thread_func = &remove_box;
            pcq_enqueue(&queue, session);
            break;
        case 7:
            // request to list all boxes 
            session->thread_func = &list_boxes;
            pcq_enqueue(&queue, session);
            break;
    } 
}

void mbroker_handle(int signum) {
    // so it doesnt go unused
    if(!signum) {
        return;
    }

    unlink(mbroker_pipe);
    
    exit(0);
}


// int main with args
// format: ./mbroker <pipe_name> <max_sessions>
int main(int argc, char **argv) {

    signal(SIGINT, mbroker_handle);
    signal(SIGPIPE, SIG_IGN);

    // check the number of arguments
    if(argc != 3) {
        fprintf(stdout,"Wrong number of arguments\n");
        exit_mbroker();
    }

    start_server(argv[1], atoi(argv[2]));
    int pipe_fd;
    ssize_t bytes_read;

    while(true) {

        pipe_fd = open(argv[1], O_RDONLY);

            // read the request from the pipe
            char request[MAX_REQUEST_SIZE];
            bytes_read = read(pipe_fd, request, sizeof(request));
            if(bytes_read < 0) {
                fprintf(stdout,"Error reading from the pipe\n");
                exit_mbroker();
            }if(bytes_read < MAX_REQUEST_SIZE) {
                //memset to 0 all the bytes that were not read
                memset(request + (size_t)bytes_read, 0, MAX_REQUEST_SIZE - (size_t)bytes_read);
            }

            close(pipe_fd);

            treat_request(request);
    }

    return 0;
}