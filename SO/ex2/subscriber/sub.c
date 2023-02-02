#include "logging.h"
#include "structs.h"


subscriber_t subscriber;

// Functions
int connect(subscriber_t *sub, char register_name[MAX_PIPE_NAME], char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME]);
int getMessages(subscriber_t *sub, char buffer[MAX_BUFFER_MESSAGE]);
int disconnect(subscriber_t *sub);

int connect(subscriber_t *sub, char register_name[MAX_PIPE_NAME], char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME]) {
    sub->server_fd = open(register_name, O_WRONLY);
    if (sub->server_fd < 0) {
        WARN("Error opening register pipe");
        close(sub->server_fd);
        return -1;
    }

    // Create the named pipe
    if (mkfifo(pipe_name, 0640) < 0) {
        WARN("Error creating named pipe");
        return -1;
    }

    // Send a request to the regsiter pipe
    char request[MAX_REQUEST_SIZE];
    build_request(2, pipe_name, message_box, request);
    if (write(sub->server_fd, request, sizeof(request)) < 0) {
        WARN("Error writing in the register pipe");
        return -1;
    }

    close(sub->server_fd);

    // Open the named pipe for reading
    sub->pipe_fd = open(pipe_name, O_RDONLY);
    if (sub->pipe_fd < 0) {
        WARN("Error opening named pipe");
        return -1;
    }

    
    return 0;
}

int getMessages(subscriber_t *sub, char buffer[MAX_BUFFER_MESSAGE]) {
    
    // Use file descriptor sets for good practice even though we only putting 1 fd in it
    fd_set read_fds;
    FD_ZERO(&read_fds);
    FD_SET(sub->pipe_fd, &read_fds);

    int available_data = select(sub->pipe_fd + 1, &read_fds, NULL, NULL, NULL);
    if(available_data < 0) {
        WARN("Error selecting");
        return -1;
    } else if (available_data == 0) {
        WARN("No data available");
        return 0;
    }

    // read the last message from the pipe
    if (read(sub->pipe_fd, buffer, MAX_BUFFER_MESSAGE) < 0) {
        WARN("Error reading from pipe");
        return -1;
    }
    return 1;
}


void sub_handler(int signum) {

    // so it doesnt go unused
    if(!signum) {
        return;
    }

    printf("\nMessages recieved during session: %d\n", subscriber.num_messages);
    close(subscriber.pipe_fd);
    unlink(subscriber.pipe_name);
    exit(0);
}


int main(int argc, char **argv) {

    signal(SIGINT, sub_handler);

    if (argc != 4) {
        WARN("Invalid number of arguments");
        return -1;
    }
    
    // format: sub <register_pipe> <pipe_name> <box_name>
    // arguments for initialization of the subscriber
    char register_name[MAX_PIPE_NAME];
    char pipe_name[MAX_PIPE_NAME];
    char message_box[MAX_BOX_NAME];
    strcpy(register_name, argv[1]);
    strcpy(pipe_name, argv[2]);
    strcpy(subscriber.pipe_name, argv[2]);
    strcpy(message_box, argv[3]);


    // Connect to the server
    if (connect(&subscriber, register_name, pipe_name, message_box) < 0) {
        WARN("Error connecting to the server");
        return -1;
    }

    char buffer[MAX_BUFFER_MESSAGE];
    char message[MAX_MESSAGE_SIZE];
    int ready_to_print;
    int code;

    while (true) {
        
        // clear the buffer
        memset(buffer, 0, sizeof(buffer));

        // get the messages from the pipe
        ready_to_print = getMessages(&subscriber, buffer);

        if (ready_to_print < 0) {
            WARN("Error getting messages");
            break;
        } else if (ready_to_print > 0) {

            // increment the number of messages received
            subscriber.num_messages++;

            // clear the message
            memset(message, 0, sizeof(message));

            // get the code from the buffer
            memcpy(&code, buffer, sizeof(uint8_t));

            if(code == (uint8_t)11) {
                fprintf(stdout, "Message box doesn't exist\n");
                subscriber.num_messages--;
                break;
            }

            // get the message in the buffer without the code
            memcpy(message, buffer + sizeof(uint8_t), MAX_MESSAGE_SIZE);

            // print the message
            fprintf(stdout, "%s\n", message);
        }
    }

    printf("\nMessages received during session: %d\n", subscriber.num_messages);
    close(subscriber.pipe_fd);
    unlink(subscriber.pipe_name);


    return 0;
}