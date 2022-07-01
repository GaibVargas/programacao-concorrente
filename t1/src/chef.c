#include <stdlib.h>

#include "chef.h"
#include "globals.h"
#include "config.h"

void *chef_run()
{
    /* Insira sua lógica aqui */
    while (TRUE)
    {
        // Verifica se todos os estudantes já se serviram
        if (globals_get_students_served() == globals_get_students()) break;
        // Checa se alguma bacia está vazia
        chef_check_food();
    }
    
    pthread_exit(NULL);
}


void chef_put_food(buffet_t *buffet, int meal_position)
{
    // Coloca 40 porções de comida na bacia
    // Ocupa a bacia, fazendo os estudantes esperarem
    pthread_mutex_lock(&m_meals[buffet->_id * 5 + meal_position]);
    buffet->_meal[meal_position] += 40;
    pthread_mutex_unlock(&m_meals[buffet->_id * 5 + meal_position]);
}
void chef_check_food()
{
    buffet_t *buffets = globals_get_buffets();
    int n_buffets = globals_get_buffets_number();
    if (buffets == NULL) return;
    // Passa por todos os buffets, checando se há comida
    for (int i = 0; i < n_buffets; i++) {
        for (int j = 0; j < 5; j++) {
            // Se a bacia está vazia, repõem comida
            if (buffets[i]._meal[j] <= 0)
                chef_put_food(&buffets[i], j);
        }
    }
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