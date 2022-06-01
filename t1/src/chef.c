#include <stdlib.h>

#include "chef.h"
#include "config.h"

void *chef_run()
{
    /* Insira sua lógica aqui */
    /*
        enquanto served_students(variável que precisa ser criada?) != all_students
        check_food
    */
    while (TRUE)
    {
        msleep(5000); /* Pode retirar este sleep quando implementar a solução! */
    }
    
    pthread_exit(NULL);
}


void chef_put_food()
{
    /* Insira sua lógica aqui */
    /*
        aqui talvez tenha um lock
        na bacia do buffet passado repor quantia (40)
    */
}
void chef_check_food()
{
    /* Insira sua lógica aqui */
    /*
        para cada buffet (usar variável do configs para saber o número de buffets)
        para cada bacia
        checar se porção > 0
        senão put_food(buffet, bacia)
    */
}

/* --------------------------------------------------------- */
/* ATENÇÃO: Não será necessário modificar as funções abaixo! */
/* --------------------------------------------------------- */

void chef_init(chef_t *self)
{
    pthread_create(&self->thread, NULL, chef_run, NULL);
}

void chef_finalize(chef_t *self)
{
    pthread_join(self->thread, NULL);
    free(self);
}