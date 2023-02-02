#include "logging.h"
#include "structs.h"


static void print_usage() {
    fprintf(stderr, "usage: \n"
                    "   manager <register_pipe_name> create <box_name>\n"
                    "   manager <register_pipe_name> remove <box_name>\n"
                    "   manager <register_pipe_name> list\n");
}


// to print error messages in given format
char error_message[MAX_MESSAGE_SIZE];

int connect(manager_t *manager, char register_name[MAX_PIPE_NAME]);
void man_create(manager_t *manager, char message_box[MAX_BOX_NAME], char pipe_name[MAX_PIPE_NAME]);
void man_remove(manager_t *manager, char message_box[MAX_BOX_NAME], char pipe_name[MAX_PIPE_NAME]);
int list_boxes(manager_t *manager, char pipe_name[MAX_PIPE_NAME]);


int connect(manager_t *manager, char register_name[MAX_PIPE_NAME]) {

    manager->server_fd = open(register_name, O_WRONLY);
    if(manager->server_fd < 0) {
        strcpy(error_message, "Error opening register pipe for writing");
        fprintf(stdout, "ERROR %s\n", error_message);
        return -1;
    }

    return 0;
}

int make_pipe(char pipe_name[MAX_PIPE_NAME]) {
    //make the fifo
    if(mkfifo(pipe_name, 0640) < 0) {
        strcpy(error_message, "Error creating the fifo");
        fprintf(stdout, "ERROR %s\n", error_message);
        return -1;
    }

    return 0;
}

void man_create(manager_t *manager, char message_box[MAX_BOX_NAME], char pipe_name[MAX_PIPE_NAME]) {
        char request[MAX_REQUEST_SIZE];

    build_request(3,pipe_name,message_box,request);

    make_pipe(pipe_name);

    if(write(manager->server_fd,request,sizeof(request)) < 0) {
        strcpy(error_message, "Error writing in the named pipe");
        fprintf(stdout, "ERROR %s\n", error_message);
        return ;
    }

    close(manager->server_fd);

    manager->pipe_fd = open(pipe_name, O_RDONLY);
    if(manager->pipe_fd < 0) {
        strcpy(error_message, "Error opening named pipe for reading");
        fprintf(stdout, "ERROR %s\n", error_message);
        return ;
    }

    char answer[MAX_ANSWER_SIZE];
    ssize_t bytes_read;
    uint8_t code;
    int32_t return_code;
    char message[MAX_MESSAGE_SIZE];

    bytes_read = read(manager->pipe_fd, answer, sizeof(answer));
    // read the request from the pipe
    if(bytes_read < 0) {
        strcpy(error_message, "Error reading from the pipe");
        fprintf(stdout, "ERROR %s\n", error_message);
        close(manager->pipe_fd);
        return;
    }else if(bytes_read != 0) {
        // clear variables
        memset(&code, 0, sizeof(uint8_t));
        memset(&return_code, 0, sizeof(int32_t));
        memset(message, 0, MAX_MESSAGE_SIZE);
        
        // fill variables
        memcpy(&code, answer, sizeof(uint8_t));
        memcpy(&return_code, answer + sizeof(uint8_t), sizeof(int32_t));
        memcpy(message, answer + sizeof(uint8_t) + sizeof(int32_t), MAX_MESSAGE_SIZE);

        if(return_code == (int32_t)-1) {
            fprintf(stdout, "ERROR %s\n", message);
            close(manager->pipe_fd);
            return ;
        }

        fprintf(stdout, "OK\n");
    }   

    close(manager->pipe_fd);
    return ;
}

void man_remove(manager_t *manager, char message_box[MAX_BOX_NAME], char pipe_name[MAX_PIPE_NAME]) {

    char request[MAX_REQUEST_SIZE];

    build_request(5,pipe_name,message_box,request);

    make_pipe(pipe_name);

    if(write(manager->server_fd,request,sizeof(request)) < 0) {
        strcpy(error_message, "Error writing in the named pipe");
        fprintf(stdout, "ERROR %s\n", error_message);
        return ;
    }

    close(manager->server_fd);

    manager->pipe_fd = open(pipe_name, O_RDONLY);
    if(manager->pipe_fd < 0) {
        strcpy(error_message, "Error opening named pipe for reading");
        fprintf(stdout, "ERROR %s\n", error_message);
        return ;
    }

    char answer[MAX_ANSWER_SIZE];
    ssize_t bytes_read;
    uint8_t code;
    int32_t return_code;
    char message[MAX_MESSAGE_SIZE];

    bytes_read = read(manager->pipe_fd, answer, sizeof(answer));
    // read the request from the pipe
    if(bytes_read < 0) {
        strcpy(error_message, "Error reading from the pipe");
        fprintf(stdout, "ERROR %s\n", error_message);
        close(manager->pipe_fd);
        return;
    }else if(bytes_read != 0) {
        // clear variables
        memset(&code, 0, sizeof(uint8_t));
        memset(&return_code, 0, sizeof(int32_t));
        memset(message, 0, MAX_MESSAGE_SIZE);
        
        // fill variables
        memcpy(&code, answer, sizeof(uint8_t));
        memcpy(&return_code, answer + sizeof(uint8_t), sizeof(int32_t));
        memcpy(message, answer + sizeof(uint8_t) + sizeof(int32_t), MAX_MESSAGE_SIZE);

        if(return_code == (int32_t)-1) {
            fprintf(stdout, "ERROR %s\n", message);
            close(manager->pipe_fd);
            return ;
        }

        fprintf(stdout, "OK\n");
    }   

    close(manager->pipe_fd);
    return ;
}

int comparator(const void *a, const void *b) {
    char *const *pa = a;
    char *const *pb = b;
    return strcmp(*pa, *pb);
}

int man_list(manager_t *manager, char pipe_name[MAX_PIPE_NAME]) {

    char request[MAX_REQUEST_SIZE];
    build_request(7, pipe_name, NULL, request);

    make_pipe(pipe_name);

    if(write(manager->server_fd,request,sizeof(request)) < 0) {
        strcpy(error_message, "Error writing in the named pipe");
        fprintf(stdout, "ERROR %s\n", error_message);
        return -1;
    }

    close(manager->server_fd);

    manager->pipe_fd = open(pipe_name, O_RDONLY);
    if(manager->pipe_fd < 0) {
        strcpy(error_message, "Error opening named pipe for reading");
        fprintf(stdout, "ERROR %s\n", error_message);
        return -1;
    }

    char answer[MAX_LIST_ANSWER];
    ssize_t bytes_read;
    uint8_t code;
    uint8_t last;
    char box_name[MAX_BOX_NAME];
    uint64_t box_size;
    uint64_t n_pubs;
    uint64_t n_subs;
    char **boxes = (char **)malloc(sizeof(char*));;
    int num_boxes = 0;

    while(true) {
            // read the request from the pipe
            bytes_read = read(manager->pipe_fd, answer, sizeof(answer));
            if(bytes_read < 0) {
                strcpy(error_message, "Error reading from the pipe");
                fprintf(stdout, "ERROR %s\n", error_message);
                exit(1);
            }else if(bytes_read != 0) {
                // fill all variables
                memcpy(&code, answer, sizeof(uint8_t));
                memcpy(&last, answer + sizeof(uint8_t), sizeof(uint8_t));
                memcpy(box_name, answer + sizeof(uint8_t) + sizeof(uint8_t), MAX_BOX_NAME);
                memcpy(&box_size, answer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME, sizeof(uint64_t));
                memcpy(&n_pubs, answer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME + sizeof(uint64_t), sizeof(uint64_t));
                memcpy(&n_subs, answer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME + sizeof(uint64_t) + sizeof(uint64_t), sizeof(uint64_t));

                if (strlen(box_name) == 0) {
                    fprintf(stdout, "NO BOXES FOUND\n");
                    break;
                }

                boxes[num_boxes] = malloc( MAX_BOX_NAME + sizeof(size_t) + sizeof(size_t) + sizeof(size_t) );

                sprintf(boxes[num_boxes] , "%s %zu %zu %zu\n", box_name, (size_t)box_size, (size_t)n_pubs, (size_t)n_subs);
                num_boxes += 1;

                //fprintf(stdout, "%s %zu %zu %zu\n", box_name, (size_t)box_size, (size_t)n_pubs, (size_t)n_subs);

                if(last == 1) {
                    break;
                }   
            }  
        }

    // sort boxes by their box_name
    qsort(boxes, (size_t)num_boxes, sizeof(char*), comparator);

    // print boxes
    for(int i = 0; i < num_boxes; i++) {
        fprintf(stdout, "%s", boxes[i]);
    }

    free(boxes);

    close(manager->pipe_fd);

    return 0;
}

int main(int argc, char **argv) {

    // formats
    //  manager <register_pipe_name> <pipe_name> create <box_name>
    //  manager <register_pipe_name> <pipe_name> remove <box_name>
    //  manager <register_pipe_name> <pipe_name> list

    // check arguments
    if(argc != 5 && argc != 4) {
        print_usage();
        return -1;
    }

    // save arguments
    char register_name[MAX_PIPE_NAME];
    char pipe_name[MAX_PIPE_NAME];
    char message_box[MAX_BOX_NAME];

    //memset everything with '\0'
    memset(register_name, 0, sizeof(register_name));
    memset(pipe_name, 0, sizeof(pipe_name));
    memset(message_box, 0, sizeof(message_box));

    // save arguments
    memcpy(register_name, argv[1], MAX_PIPE_NAME);
    memcpy(pipe_name, argv[2], MAX_PIPE_NAME);

    // create manager
    manager_t manager;

    // connect to server
    if(connect(&manager, register_name) < 0) {
        strcpy(error_message, "Error connecting to server");
        fprintf(stdout, "ERROR %s\n", error_message);
        return -1;
    }

    // check argv[4] and the act accordingly
    if(strcmp(argv[3], "create") == 0) {
        memcpy(message_box, argv[4], MAX_BOX_NAME);
        man_create(&manager, message_box, pipe_name);
    } else if(strcmp(argv[3], "remove") == 0) {
        memcpy(message_box, argv[4], MAX_BOX_NAME);
        man_remove(&manager, message_box, pipe_name);
    } else if(strcmp(argv[3], "list") == 0) {
        man_list(&manager, pipe_name);
    } else {
        print_usage();
    }

    unlink(pipe_name);

    return 0;

}
