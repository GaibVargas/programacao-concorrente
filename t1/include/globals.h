#ifndef __GLOBALS_H__
#define __GLOBALS_H__

#include <pthread.h>
#include "queue.h"
#include "table.h"
#include "buffet.h"

// Controlam o id do buffet com lugar vago na fila e o lado da fila
extern int global_id_buffet;
extern char global_left_or_right;

// Controla o acesso as variáveis global_id_buffet e global_left_or_right
extern pthread_mutex_t m_buffet_detail;
// Controla o acesso a fila
extern pthread_mutex_t m_external_queue;
// Array de mutexes que controlam o acesso as mesas
// Existente para o estudante decrementar o número de assentos vagos da mesa
extern pthread_mutex_t *m_tables;
// Array de mutexes que controla o acesso a bacia de comida
extern pthread_mutex_t *m_meals;
// Semáforos que controlam a produção e consumo das variáveis global_id_buffet e global_left_or_right
extern sem_t s_buffet_detail_producer;
extern sem_t s_buffet_detail_consumer;
// Semáforo que determina se uma posição na fila (interna) do buffet está livre
// Existe para que um estudante não apague o registro de outro na fila do buffet
extern sem_t *s_buffet_queue_position;
// Semáforo que controla o acesso a área das mesas
extern sem_t s_table_seats;

/**
 * @brief Incrementa o número de estudantes que já sairam do restaurante (de modo global)
 *  
 */
extern void globals_student_leave_restaurant();

/**
 * @brief Retorna o número de estudantes que já sairam do restaurante (de modo global)
 * 
 * @return int 
 */
extern int globals_get_students_leave_restaurant();
/**
 * @brief Insere o número de buffets (de modo global)
 * 
 * @param buffet_number 
 */
extern void globals_set_buffets_number(int buffet_number);

/**
 * @brief Retorna o número de buffets (de modo global)
 * 
 * @return int 
 */
extern int globals_get_buffets_number();

/**
 * @brief Insere o número de mesas (de modo global)
 * 
 * @param table_number 
 */
extern void globals_set_tables_number(int table_number);

/**
 * @brief Retorna o número de mesas (de modo global)
 * 
 * @return int 
 */
extern int globals_get_tables_number();

/**
 * @brief Incrementa o número de estudantes que se serviram (de modo global)
 *  
 */
extern void globals_student_served();

/**
 * @brief Retorna o número de estudantes que se serviram (de modo global)
 * 
 * @return int 
 */
extern int globals_get_students_served();

/**
 * @brief Inicia uma fila (de modo global)
 * 
 * @param queue 
 */
extern void globals_set_queue(queue_t *queue);

/**
 * @brief Retorna uma fila (de modo global)
 * 
 * @return queue_t* 
 */
extern queue_t *globals_get_queue();

/**
 * @brief Insere o número de alunos (de modo global)
 * 
 */
extern void globals_set_students(int number);

/**
 * @brief Retorna o número de alunos (de modo global)
 * 
 * @return int 
 */

extern int globals_get_students();

/**
 * @brief Inicia um array de mesas (de modo global).
 * 
 * @param t 
 */
extern void globals_set_table(table_t *t);

/**
 * @brief Retorna um array de mesas (de modo global)
 * 
 * @return table_t* 
 */
extern table_t *globals_get_table();


/**
 * @brief Finaliza todas as variáveis globais.
 * 
 */
extern void globals_finalize();

/**
 * @brief Inicia um array de buffets (de modo global)
 * 
 */
extern void globals_set_buffets(buffet_t *buffets_ref);

/**
 * @brief Retorna um array de buffets (de modo global)
 * 
 * @return buffet_t* 
 */
extern buffet_t *globals_get_buffets();

#endif