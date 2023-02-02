#include "structs.h"


void build_message(uint8_t code, char message[MAX_MESSAGE_SIZE], char* buffer) {
    // use memcpy to copy the paramaters to the buffer
    memcpy(buffer, &code, sizeof(uint8_t)); 
    memcpy(buffer + sizeof(uint8_t), message, strlen(message));

    return ;
}

void build_request(uint8_t code, char pipe_name[MAX_PIPE_NAME], char message_box[MAX_BOX_NAME], char* buffer) {
    // use memcpy to copy the paramaters to the buffer
    memcpy(buffer, &code, sizeof(uint8_t));
    memcpy(buffer + sizeof(uint8_t), pipe_name, MAX_PIPE_NAME);
    if(message_box == NULL)
        return;
    memcpy(buffer + sizeof(uint8_t) + MAX_PIPE_NAME, message_box, MAX_BOX_NAME);

    return;    
}

void build_answer_to_list(uint8_t code, uint8_t last, char box_name[MAX_BOX_NAME], uint64_t box_size, uint64_t n_pubs, uint64_t n_subs, char *buffer) {
    // use memcpy to copy the paramaters to the buffer
    memcpy(buffer, &code, sizeof(uint8_t));
    memcpy(buffer + sizeof(uint8_t), &last, sizeof(uint8_t));
    memcpy(buffer + sizeof(uint8_t) + sizeof(uint8_t), box_name, MAX_BOX_NAME);
    memcpy(buffer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME, &box_size, sizeof(uint64_t));
    memcpy(buffer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME + sizeof(uint64_t), &n_pubs, sizeof(uint64_t));
    memcpy(buffer + sizeof(uint8_t) + sizeof(uint8_t) + MAX_BOX_NAME + sizeof(uint64_t) + sizeof(uint64_t), &n_subs, sizeof(uint64_t));

    return;
}

void build_answer_to_box(uint8_t code, int32_t return_code, const char *err_message, char* buffer) {
    // use memcpy to copy the paramaters to the buffer
    memcpy(buffer, &code, sizeof(uint8_t));
    memcpy(buffer + sizeof(uint8_t), &return_code, sizeof(int32_t));
    memcpy(buffer + sizeof(uint8_t) + sizeof(int32_t), err_message, strlen(err_message) + 1);

    return;
}

//adds the box to the linked list and initialize all the elementsto 0
void add_box(node_t **head,char box_name[MAX_BOX_NAME]) {
    //in case of first
    if(*head == NULL) {
        (*head) = malloc(sizeof(node_t));
        pthread_mutex_init(&(*head)->mutex, NULL);
        pthread_cond_init(&(*head)->cond, NULL);
        strcpy((*head)->box_name, box_name);
        (*head)->next = NULL;
        (*head)->n_subs = 0;
        (*head)->n_pubs = 0;
        (*head)->box_size = 0;
        return;
    } else {
        node_t *current = *head;
        while(current->next != NULL) {
            current = current->next;
        }

        current->next = malloc(sizeof(node_t));
        pthread_mutex_init(&(current->next->mutex), NULL);
        pthread_cond_init(&(current->next->cond), NULL);
        strcpy(current->next->box_name, box_name);
        current->next->next = NULL;
        current->next->n_subs = 0;
        current->next->n_pubs = 0;
        current->next->box_size = 0;
        return;
    }
}

//removes the box from the linked list
int rm_box(node_t **head ,char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    node_t *prev = NULL;

    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            if(current->n_subs != 0 || current->n_pubs != 0) {
                return -1;
            }
            if(prev == NULL) {
                *head = current->next;
            } else {
                prev->next = current->next;
            }
            free(current);
            return 0;
        }
        prev = current;
        current = current->next;
    }

    return -1;
}

//returns the node with the box_name
node_t *get_box(node_t **head ,char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

//adds the publisher to the box
void add_pub(node_t **head, char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            current->n_pubs++;
            return;
        }

        current = current->next;
    }
}

void rm_pub(node_t **head, char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            current->n_pubs--;
            return;
        }

        current = current->next;
    }
}

void add_sub(node_t **head, char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            current->n_subs++;
            return;
        }
        current = current->next;
    }
}

void rm_sub(node_t **head, char box_name[MAX_BOX_NAME]) {
    node_t *current = *head;
    while(current != NULL) {
        if(strcmp(current->box_name, box_name) == 0) {
            current->n_subs--;
        }
        current = current->next;
    }
}
