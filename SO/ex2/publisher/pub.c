#include "logging.h"
#include "structs.h"


publisher_t publisher;

// Functions
int connect(publisher_t *pub, char register_name[MAX_PIPE_NAME], char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME]);
int publish(publisher_t *pub, char message[MAX_MESSAGE_SIZE]);
int disconnect(publisher_t *pub);

int connect(publisher_t *pub, char register_name[MAX_PIPE_NAME], char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME]) {


    // Open the register pipe
    pub->server_fd = open(register_name, O_WRONLY);
    if(pub->server_fd < 0) {
        printf("Error opening register pipe for writing\n");
        close(pub->server_fd);
        return -1;
    }

    strcpy(pub->message_box,message_box);

    char request[MAX_REQUEST_SIZE];
    build_request(1, pipe_name, message_box, request);

    // make the fifo
    if(mkfifo(pipe_name, 0640) < 0) {
        printf("Error creating the fifo\n");
        return -1;
    }

    if(write(pub->server_fd,request,sizeof(request)) <= 0) {
        printf("Error writing in the register pipe\n");
        return -1;
    }

    close(pub->server_fd);

    return 0;
}

int publish(publisher_t *pub, char message[MAX_MESSAGE_SIZE]) {
    
    // create a message and send it to the pipe
    char buffer[MAX_BUFFER_MESSAGE];
    memset(buffer, 0, MAX_BUFFER_MESSAGE);
    build_message(9, message, buffer);

    if(write(pub->pipe_fd, buffer, strlen(buffer)) < 0) {
        printf("Error writing in the pipe\n");
        return -1;
    }

    return 0;
}

int wait_message(char message[MAX_MESSAGE_SIZE]) {

    // wait for a message from the user, avoid unused return value warning.
    if(fgets(message, MAX_MESSAGE_SIZE, stdin) == NULL){};

    message[strcspn(message, "\n")] = 0;

    return 0;
}

int disconnect(publisher_t *pub) { return close(pub->pipe_fd); }

void eof_handler(int signum) {
    //so it doesnt go unused
    if(!signum) {
        return;
    }

    printf("\nEOF received, closing publisher\n");
    close(publisher.pipe_fd);
    unlink(publisher.pipe_name);
    exit(0);
}


int main(int argc, char **argv) {

    signal(SIGTSTP, eof_handler);

    // check the number of arguments
    if(argc != 4) {
        printf("Wrong number of arguments\n");
        exit(1);
    }

    // get the arguments from the command
    char register_name[MAX_PIPE_NAME];
    char pipe_name[MAX_PIPE_NAME];
    char message_box[MAX_BOX_NAME];

    strcpy(register_name, argv[1]);
    strcpy(pipe_name, argv[2]);
    strcpy(message_box, argv[3]);

    // connect to the server
    if(connect(&publisher, register_name, pipe_name, message_box) < 0) {
        printf("Error connecting to the server\n");
        return -1;
    }

    char message[MAX_MESSAGE_SIZE];

    // open the pipe for writing
    publisher.pipe_fd = open(pipe_name, O_WRONLY);

    if(publisher.pipe_fd < 0) {
        printf("Error opening the pipe for writing\n");
        return -1;
    }


    strcpy(publisher.pipe_name, pipe_name);

    while(true) {
        // clear message
        memset(message, 0, MAX_MESSAGE_SIZE);

        // wait for a message from the user
        wait_message(message);

        // check if the message is empty
        if(strlen(message) > 0) {

            if(publish(&publisher, message) < 0) {
                printf("Error publishing the message\n");
                break;
            }
        }
    }
    return 0;
}
