#include <stdio.h>
#include <semaphore.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include "banco.h"

// Faz uma transferência de valor unidades monetárias da conta origem
// para a conta destino. Se a conta origem tiver saldo insuficiente, o
// saldo fica negativo, simbolizando cheque especial.  
// 
// Essa função é "unsafe": ela não aplica nenhum mecanismo de
// sincronização e pode produzir valores errados se utilizada
// concorrentemente com a mesma conta.
//
// Definida em helper.c

// Garante que os caixas ao possuirem seus recursos (contas de origem e destino)
// façam isso de forma "atômica", impedindo assim o deadlock
// No pior caso há 1 thread executando, no melhor caso há 2
pthread_mutex_t possuir_contas;

extern void transferir_unsafe(conta_t *origem, conta_t *destino, double valor);

void transferir(conta_t *origem, conta_t *destino, double valor);

// Thread que faz  transferências aleatórias. Definida em helper.c
void* caixa_func(void *arg);

// Versão thread-safe da função transferir_unsafe.
void transferir(conta_t *origem, conta_t *destino, double valor) {
    pthread_mutex_lock(&possuir_contas);
    pthread_mutex_lock(&origem->mutex);
    pthread_mutex_lock(&destino->mutex);
    pthread_mutex_unlock(&possuir_contas);

    transferir_unsafe(origem, destino, valor);

    pthread_mutex_unlock(&destino->mutex);
    pthread_mutex_unlock(&origem->mutex);
}

int main(int argc, char* argv[]) {
    pthread_mutex_init(&possuir_contas, NULL);

    // Cria as contas com algum saldo e inicializa o mutex de cada conta
    for (int i = 0; i < NUM_CONTAS; i++) {
        contas[i].id = i;
        contas[i].saldo = 1000.00;
        pthread_mutex_init(&contas[i].mutex, NULL);
    }
  
    // Cria as threads
    pthread_t caixas[NUM_CAIXAS];
    for (int i = 0; i < NUM_CAIXAS; i++)
        pthread_create(&caixas[i], NULL, caixa_func, NULL);
  
    // Esperar as threads terminarem
    for (int i = 0; i < NUM_CAIXAS; i++)
        pthread_join(caixas[i], NULL);
  
    // Destroi os mutexes
    for (int i = 0; i < NUM_CONTAS; i++)
        pthread_mutex_destroy(&contas[i].mutex);
    
    pthread_mutex_destroy(&possuir_contas);
  
    return 0;
}
