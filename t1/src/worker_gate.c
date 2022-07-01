#include <stdlib.h>

#include "worker_gate.h"
#include "globals.h"
#include "config.h"

char left_or_right = 'L';
// Controla se os primeiros estudantes já entraram
// Objetivo: Colocar os primeiros estudantes em filas diferentes
int first_horda = 0;

int id_buffet = 0;

int worker_gate_look_queue()
{
    queue_t *queue = globals_get_queue();
    return queue->_length > 0;
}

void worker_gate_remove_student()
{
    // Remove estudante da primeira posição da fila
    pthread_mutex_lock(&m_external_queue);
    queue_t *queue = globals_get_queue();
    student_t *student = queue_remove(queue);
    pthread_mutex_unlock(&m_external_queue);
    // Verifica se o buffet acabou de abrir
    // Se sim, coloca os primeiros estudantes em filas diferentes
    if (first_horda < globals_get_buffets_number() * 2) {
        // Configura informações dos estudantes (buffet e lado da fila)
        student->left_or_right = left_or_right;
        student->_id_buffet = id_buffet;
        if (left_or_right == 'R') id_buffet++;
        left_or_right = left_or_right == 'L' ? 'R' : 'L';
        first_horda++;
    } else { // O buffet já foi ocupado pelos primeiros estudantes da fila externa
        // Configura informações dos estudantes (buffet e lado da fila)
        sem_wait(&s_buffet_detail_consumer);
        student->left_or_right = global_left_or_right;
        student->_id_buffet = global_id_buffet;
        sem_post(&s_buffet_detail_producer);
    }
    // Insere estudante na fila (interna) do buffet
    buffet_queue_insert(globals_get_buffets(), student);
}

int worker_gate_look_buffet()
{
    buffet_t *buffets = globals_get_buffets();
    int buffets_number = globals_get_buffets_number();
    // Verifica se o buffet está disponível a receber um novo estudante na fila
    for (int i = 0; i < buffets_number; i++) {
        if (!buffets[i].queue_left[0] || !buffets[i].queue_right[0]) {
            return TRUE;
        }
    }
    return FALSE;
}

void *worker_gate_run(void *arg)
{
    int all_students_entered;
    int number_students;

    int students_on_queue = 0;
    int buffet_has_slot = 0;

    number_students = *((int *)arg);
    all_students_entered = number_students > 0 ? FALSE : TRUE;

    while (all_students_entered == FALSE)
    {
        // Verifica a fila externa
        students_on_queue = worker_gate_look_queue();
        // Há estudantes na fila externa?
        if (students_on_queue) {
            buffet_has_slot = worker_gate_look_buffet();
            // Há espaço em algum buffet?
            if (buffet_has_slot) {
                // Remove estudante da fila externa e o coloca na fila interna de algum buffet
                worker_gate_remove_student();
                number_students--;
                // Verifica se ainda há estudantes na fila externa
                all_students_entered = number_students > 0 ? FALSE : TRUE;
            }
        }
    }
    // Cria espaço para os estudantes no buffet que vão caminhar após o fechamento da catraca
    // Resolve um bug de quando o worker_gate sair, os últimos estudantes ficarem travados na posição 2 do buffet
    // Mulplicação por 2 pois são duas filas por buffet
    for (int i = 0; i < globals_get_buffets_number() * 2; i++)
        sem_post(&s_buffet_detail_producer);
    pthread_exit(NULL);
}

void worker_gate_init(worker_gate_t *self)
{
    int number_students = globals_get_students();
    pthread_create(&self->thread, NULL, worker_gate_run, &number_students);
}

void worker_gate_finalize(worker_gate_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}

void worker_gate_insert_queue_buffet(student_t *student)
{
    // Insere estudante na fila externa do buffet
    pthread_mutex_lock(&m_external_queue);
    queue_t *queue = globals_get_queue();
    queue_insert(queue, student);
    pthread_mutex_unlock(&m_external_queue);
}