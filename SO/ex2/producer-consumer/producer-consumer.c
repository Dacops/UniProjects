#include "producer-consumer.h"
#include "structs.h"

#include <pthread.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

int pcq_create(pc_queue_t *queue, size_t capacity)
{
    queue->pcq_buffer = malloc(capacity * sizeof(void*));
    if (queue->pcq_buffer == NULL) {
        return -1;
    }

    queue->pcq_capacity = capacity;

    pthread_mutex_init(&queue->pcq_current_size_lock, NULL);
    queue->pcq_current_size = 0;

    pthread_mutex_init(&queue->pcq_head_lock, NULL);
    queue->pcq_head = 0;

    pthread_mutex_init(&queue->pcq_tail_lock, NULL);
    queue->pcq_tail = 0;

    pthread_mutex_init(&queue->pcq_pusher_condvar_lock, NULL);
    pthread_cond_init(&queue->pcq_pusher_condvar, NULL);

    pthread_mutex_init(&queue->pcq_popper_condvar_lock, NULL);
    pthread_cond_init(&queue->pcq_popper_condvar, NULL);

    return 0;
}

int pcq_destroy(pc_queue_t *queue)
{
    free(queue->pcq_buffer);
    queue->pcq_buffer = NULL;

    pthread_mutex_destroy(&queue->pcq_current_size_lock);
    pthread_mutex_destroy(&queue->pcq_head_lock);
    pthread_mutex_destroy(&queue->pcq_tail_lock);
    pthread_mutex_destroy(&queue->pcq_pusher_condvar_lock);
    pthread_mutex_destroy(&queue->pcq_popper_condvar_lock);

    pthread_cond_destroy(&queue->pcq_pusher_condvar);
    pthread_cond_destroy(&queue->pcq_popper_condvar);

    return 0;
}

int pcq_enqueue(pc_queue_t *queue, void *elem) {
    pthread_mutex_lock(&queue->pcq_pusher_condvar_lock);
    while (queue->pcq_current_size == queue->pcq_capacity) {
        pthread_cond_wait(&queue->pcq_pusher_condvar, &queue->pcq_pusher_condvar_lock);
    }
    pthread_mutex_unlock(&queue->pcq_pusher_condvar_lock);

    pthread_mutex_lock(&queue->pcq_current_size_lock);
    queue->pcq_current_size++;
    pthread_mutex_unlock(&queue->pcq_current_size_lock);

    pthread_mutex_lock(&queue->pcq_tail_lock);
    queue->pcq_buffer[queue->pcq_tail] = elem;
    queue->pcq_tail = (queue->pcq_tail + 1) % queue->pcq_capacity;
    pthread_mutex_unlock(&queue->pcq_tail_lock);

    pthread_mutex_lock(&queue->pcq_popper_condvar_lock);
    pthread_cond_signal(&queue->pcq_popper_condvar);
    pthread_mutex_unlock(&queue->pcq_popper_condvar_lock);

    return 0;
}

void *pcq_dequeue(pc_queue_t *queue) {
    pthread_mutex_lock(&queue->pcq_popper_condvar_lock);
    while (queue->pcq_current_size == 0) {
        pthread_cond_wait(&queue->pcq_popper_condvar, &queue->pcq_popper_condvar_lock);
    }
    pthread_mutex_unlock(&queue->pcq_popper_condvar_lock);

    pthread_mutex_lock(&queue->pcq_current_size_lock);
    queue->pcq_current_size--;
    pthread_mutex_unlock(&queue->pcq_current_size_lock);

    pthread_mutex_lock(&queue->pcq_head_lock);
    void *elem = queue->pcq_buffer[queue->pcq_head];
    queue->pcq_head = (queue->pcq_head + 1) % queue->pcq_capacity;
    pthread_mutex_unlock(&queue->pcq_head_lock);

    pthread_mutex_lock(&queue->pcq_pusher_condvar_lock);
    pthread_cond_signal(&queue->pcq_pusher_condvar);
    pthread_mutex_unlock(&queue->pcq_pusher_condvar_lock);

    return elem;
}