#include <stdlib.h>
#include "globals.h"

queue_t *students_queue = NULL;
table_t *table = NULL;
buffet_t *buffets_ref = NULL;

// Descritas em globals.h
pthread_mutex_t m_external_queue;
pthread_mutex_t m_buffet_detail;
pthread_mutex_t *m_tables;
pthread_mutex_t *m_meals;
pthread_mutex_t m_students_served;
pthread_mutex_t m_students_leave;
sem_t s_buffet_detail_producer;
sem_t s_buffet_detail_consumer;
sem_t *s_buffet_queue_position;
sem_t s_table_seats;

// Variáveis para controlar qual buffet tem espaço na fila
// e qual das filas está vaga (direita ou esquerda)
// Objetivo: homogeneizar a ocupação das filas
int global_id_buffet;
char global_left_or_right;

int students_number = 0;
int students_served = 0;
int students_leave = 0;
int buffets_number = 0;
int tables_number = 0;

void globals_student_leave_restaurant() {
    pthread_mutex_lock(&m_students_leave);
    students_leave++;
    pthread_mutex_unlock(&m_students_leave);
}

int globals_get_students_leave_restaurant() {
    return students_leave;
}

void globals_student_served()
{
    pthread_mutex_lock(&m_students_served);
    students_served++;
    pthread_mutex_unlock(&m_students_served);
}

int globals_get_students_served()
{
    return students_served;
}

void globals_set_tables_number(int table_number)
{
    tables_number = table_number;
    m_tables = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t) * table_number);
    // Inicia mutexes das mesas, já que vários estudantes podem tentar sentar simultâneamente
    for (int i = 0; i < table_number; i++)
        pthread_mutex_init(&m_tables[i], NULL);
}

int globals_get_tables_number()
{
    return tables_number;
}

void globals_set_buffets_number(int buffet_number)
{
    buffets_number = buffet_number;
    // As posições são controlados por semáforos agrupados em um array
    // Multiplicação por dois pois cada buffet possui duas filas
    // Multiplicação por cinco pois cada fila possui 5 posições
    int number_queue_position = buffet_number * 2 * 5;
    s_buffet_queue_position = (sem_t*)malloc(sizeof(sem_t) * number_queue_position);
    // Inicia os semáforos das posições, na configuração livre
    for (int i = 0; i < number_queue_position; i++)
        sem_init(&s_buffet_queue_position[i], 0, 1);
    // Mutexes para acessar as bacias de comida
    // Multiplicação por cinco pois cada buffet possui 5 bacias de comida
    m_meals = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t) * buffet_number * 5);
    for (int i = 0; i < buffet_number * 5; i++)
        pthread_mutex_init(&m_meals[i], NULL);
}

int globals_get_buffets_number()
{
    return buffets_number;
}

void globals_set_queue(queue_t *queue)
{
    // Inicia mutex para acessar a fila externa
    pthread_mutex_init(&m_external_queue, NULL);
    // Inicia mutex para acessar as variáveis que configuram
    // qual é o buffet que está com espaço vago, e qual das filas é
    pthread_mutex_init(&m_buffet_detail, NULL);
    // Inicia semáforos que controlam a produção e consumo das variáveis
    // citadas acima
    sem_init(&s_buffet_detail_consumer, 0, 0);
    sem_init(&s_buffet_detail_producer, 0, 1);
    students_queue = queue;
}

queue_t *globals_get_queue()
{
    return students_queue;
}

void globals_set_table(table_t *t)
{
    table = t;
}

table_t *globals_get_table()
{
    return table;
}


void globals_set_students(int number)
{
    pthread_mutex_init(&m_students_served, NULL);
    pthread_mutex_init(&m_students_leave, NULL);
    students_number = number;
}

int globals_get_students()
{
    return students_number;
}

void globals_set_buffets(buffet_t *buffets)
{
    buffets_ref = buffets;
}

buffet_t *globals_get_buffets()
{
    return buffets_ref;
}


/**
 * @brief Finaliza todas as variáveis globais que ainda não foram liberadas.
 *  Se criar alguma variável global que faça uso de mallocs, lembre-se sempre de usar o free dentro
 * dessa função.
 */
void globals_finalize()
{
    pthread_mutex_destroy(&m_external_queue);
    pthread_mutex_destroy(&m_buffet_detail);
    pthread_mutex_destroy(&m_students_served);
    pthread_mutex_destroy(&m_students_leave);
    sem_destroy(&s_buffet_detail_consumer);
    sem_destroy(&s_buffet_detail_producer);
    sem_destroy(&s_table_seats);
    for (int i = 0; i < globals_get_buffets_number() * 2 * 5; i++)
        sem_destroy(&s_buffet_queue_position[i]);

    for (int i = 0; i < globals_get_buffets_number() * 5; i++)
        pthread_mutex_destroy(&m_meals[i]);

    for (int i = 0; i < globals_get_tables_number(); i++)
        pthread_mutex_destroy(&m_tables[i]);

    free(table);
    free(s_buffet_queue_position);
    free(m_tables);
}