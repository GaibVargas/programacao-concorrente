#include <time.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

#include "student.h"
#include "config.h"
#include "worker_gate.h"
#include "globals.h"
#include "table.h"

void* student_run(void *arg)
{
    student_t *self = (student_t*) arg;
    table_t *tables = globals_get_table();
    // Insere estudante na fila(externa) do buffet
    worker_gate_insert_queue_buffet(self);
    // Espera ser liberado para ocupar o buffet, e continuar sua execução
    sem_wait(&self->sem_serve);
    // Passa por todas as bacias se servindo
    for (int i = 0; i < 5; i++) {
        student_serve(self);
    }
    // Informa ao sistema que mais um estudante terminou de se servir
    globals_student_served();
    student_seat(self, tables);
    student_leave(self, tables);
    // Informa ao sistema que mais um estudante está saindo do restaurante
    globals_student_leave_restaurant();
    pthread_exit(NULL);
};

void student_seat(student_t *self, table_t *table)
{
    // Tenta sentar numa mesa caso haja disponibilidade
    sem_wait(&s_table_seats);
    int n_tables = globals_get_tables_number();
    // Checa quais das mesas possue lugar
    for (int i = 0; i < n_tables; i++) {
        if (table[i]._empty_seats) {
            // Ocupa espaço na mesa
            pthread_mutex_lock(&m_tables[i]);
            table[i]._empty_seats -= 1;
            pthread_mutex_unlock(&m_tables[i]);
            self->_id_table = table[i]._id;
            break;
        }
    }
    // Considerando que o estudante fica ao menos 5 segundos sentado na mesa
    msleep(5000);
}

void student_serve(student_t *self)
{
    // Se a bacia for uma comida que o estudante quer, ele se serve
    if (self->_wishes[self->_buffet_position]) {
        buffet_t *buffets = globals_get_buffets();
        // Considerando que o aluno demora ao menos 2 segundos para se servir
        msleep(2000);
        // Retira uma porção de comida da bacia
        pthread_mutex_lock(&m_meals[self->_id_buffet * 5 + self->_buffet_position]);
        buffets[self->_id_buffet]._meal[self->_buffet_position] -= 1;
        pthread_mutex_unlock(&m_meals[self->_id_buffet * 5 + self->_buffet_position]);
    }
    // Após se servir o estudante anda para a próxima posição da fila do buffet
    buffet_next_step(globals_get_buffets(), self);
}

void student_leave(student_t *self, table_t *table)
{
    // Desocupa um lugar da mesa
    pthread_mutex_lock(&m_tables[self->_id_table]);
    table[self->_id_table]._empty_seats += 1;
    pthread_mutex_unlock(&m_tables[self->_id_table]);
    // Libera semáforo das mesas
    sem_post(&s_table_seats);
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

student_t *student_init()
{
    student_t *student = malloc(sizeof(student_t));
    student->_id = rand() % 1000;
    student->_buffet_position = -1;
    int none = TRUE;
    for (int j = 0; j <= 4; j++)
    {
        student->_wishes[j] = _student_choice();
        if(student->_wishes[j] == 1) none = FALSE;
    }

    if(none == FALSE){
        /* O estudante só deseja proteína */
        student->_wishes[3] = 1;
    }

    sem_init(&student->sem_serve, 0, 0);

    return student;
};

void student_finalize(student_t *self){
    sem_destroy(&self->sem_serve);
    free(self);
};


pthread_t students_come_to_lunch(int number_students)
{
    pthread_t lets_go;
    pthread_create(&lets_go, NULL, _all_they_come, &number_students);
    return lets_go;
}

/**
 * @brief Função (privada) que inicializa as threads dos alunos.
 * 
 * @param arg 
 * @return void* 
 */
void* _all_they_come(void *arg)
{
    int number_students = *((int *)arg);
    
    student_t *students[number_students];

    for (int i = 0; i < number_students; i++)
    {
        students[i] = student_init();                                               /* Estudante é iniciado, recebe um ID e escolhe o que vai comer*/
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_create(&students[i]->thread, NULL, student_run, students[i]);       /*  Cria as threads  */
    }

    for (int i = 0; i < number_students; i++)
    {
        pthread_join(students[i]->thread, NULL);                                    /*  Aguarda o término das threads   */
    }

    for (int i = 0; i < number_students; i++)
    {
        student_finalize(students[i]);                                              /*  Libera a memória de cada estudante  */
    }

    pthread_exit(NULL);
}

/**
 * @brief Função que retorna as escolhas dos alunos, aleatoriamente (50% para cada opção)
 *        retornando 1 (escolhido) 0 (não escolhido). É possível que um aluno não goste de nenhuma opção
 *         de comida. Nesse caso, considere que ele ainda passa pela fila, como todos aqueles que vão comer.
 * @return int 
 */
int _student_choice()
{
    float prob = (float)rand() / RAND_MAX;
    return prob > 0.51 ? 1 : 0;
}