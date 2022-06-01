#include <stdlib.h>

#include "worker_gate.h"
#include "globals.h"
#include "config.h"



void worker_gate_look_queue()
{
    /* Insira aqui sua lógica */
    /*
        Olha a queue._length (esse queue também precisa de um MUTEX)
        Retorna true ou false
        True -> quando ainda há fila
        False -> quando não há fila (dá um break no loop infinito)    
    */
}

void worker_gate_remove_student()
{
    /* Insira aqui sua lógica */
    /* Versão 1.0
        Pega o student do queue de fora do RU (não esquecer o MUTEX do queue)
        Enviar student e buffet para insert_queue_buffet
    */
   /*   Versão 2.0
        Pega student do queue geral (MUTEX)
        Faz buffet_queue_insert para cada buffet
        Somar number_students
   */
}

void worker_gate_look_buffet()
{
    /* Insira aqui sua lógica */
    /*
        Consulta todos os buffets
        Consulta o fim da fila de todos os buffets
        Se o final da fila for 0 -> chama o remove_students
        Senão continua o loop
    */
}

void *worker_gate_run(void *arg)
{
    int all_students_entered;
    int number_students;

    number_students = *((int *)arg);
    all_students_entered = number_students > 0 ? FALSE : TRUE;

    while (all_students_entered == FALSE)
    {
        /*  Versã0 1.0
            Chama look_queue e avalia (break ou continua)
            Chama look_buffet
            Avaliar all_students_entered novamente
        */
        /*  Versã0 2.0
            Chama look_queue e avalia (break ou continua)
            Chama look_buffet
        */
        worker_gate_look_queue();
        worker_gate_look_buffet();
        worker_gate_remove_student();
        msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }

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
    /* Insira aqui sua lógica */
    /*  Versão 1.0
        Identificar o lado do buffet que está livre
        Atualizar student (_id_buffet, left_or_right, _buffet_position)
        Atualizar buffet (queue do lado certo recebe o id do student) essa parte pode ter MUTEX
        Somar number_students
    */
   /*   Versão 2.0
        Faz buffet_queue_insert para cada buffet
        Se TRUE em alguma -> somar number_students e retorna
        Senão colocar student no queue geral (MUTEX)
   */
}