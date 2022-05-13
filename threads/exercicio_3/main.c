#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>
#include <math.h>

// Lê o conteúdo do arquivo filename e retorna um vetor E o tamanho dele
// Se filename for da forma "gen:%d", gera um vetor aleatório com %d elementos
//
// +-------> retorno da função, ponteiro para vetor malloc()ado e preenchido
// | 
// |         tamanho do vetor (usado <-----+
// |         como 2o retorno)              |
// v                                       v
double* load_vector(const char* filename, int* out_size);


// Avalia se o prod_escalar é o produto escalar dos vetores a e b. Assume-se
// que ambos a e b sejam vetores de tamanho size.
void avaliar(double* a, double* b, int size, double prod_escalar);

typedef struct
{
    int start, end, partial_result;
    double *a, *b;
} operand_t;

operand_t *create_operand(int i, int size, int n_threads, double *a, double *b)
{
    operand_t *operand = malloc(sizeof(operand_t));
    operand->start = floor(i * size / n_threads);
    operand->end = floor((size * (i + 1)) / n_threads);
    operand->partial_result = 0;
    operand->a = a;
    operand->b = b;
    return operand;
}

void *calculate(void *args)
{
    operand_t operand = *(operand_t *)args;
    for (int i = operand.start; i < operand.end; i++)
    {
        ((operand_t *)args)->partial_result += operand.a[i] * operand.b[i];
    }
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
    srand(time(NULL));

    //Temos argumentos suficientes?
    if(argc < 4) {
        printf("Uso: %s n_threads a_file b_file\n"
               "    n_threads    número de threads a serem usadas na computação\n"
               "    *_file       caminho de arquivo ou uma expressão com a forma gen:N,\n"
               "                 representando um vetor aleatório de tamanho N\n", 
               argv[0]);
        return 1;
    }
  
    //Quantas threads?
    int n_threads = atoi(argv[1]);
    if (!n_threads) {
        printf("Número de threads deve ser > 0\n");
        return 1;
    }
    //Lê números de arquivos para vetores alocados com malloc
    int a_size = 0, b_size = 0;
    double* a = load_vector(argv[2], &a_size);
    if (!a) {
        //load_vector não conseguiu abrir o arquivo
        printf("Erro ao ler arquivo %s\n", argv[2]);
        return 1;
    }
    double* b = load_vector(argv[3], &b_size);
    if (!b) {
        printf("Erro ao ler arquivo %s\n", argv[3]);
        return 1;
    }
    
    //Garante que entradas são compatíveis
    if (a_size != b_size) {
        printf("Vetores a e b tem tamanhos diferentes! (%d != %d)\n", a_size, b_size);
        return 1;
    }

    //Calcula produto escalar. Paralelize essa parte
    if (n_threads > a_size) n_threads = a_size;
    operand_t *operands_array[n_threads];
    int operands_size = 0;
    pthread_t threads[n_threads];

    for (int i = 0; i < n_threads; ++i)
    {
        operand_t *operand = create_operand(i, a_size, n_threads, a, b);
        // Registra os operados para poder usar o free depois
        operands_array[operands_size] = operand;
        operands_size++;
        pthread_create(&threads[i], NULL, calculate, (void *)operand);
    }

    double result = 0;    
    for (int i = 0; i < n_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    for (int i = 0; i < operands_size; i++) {
        result += operands_array[i]->partial_result;
    }
    
    //    +---------------------------------+
    // ** | IMPORTANTE: avalia o resultado! | **
    //    +---------------------------------+
    avaliar(a, b, a_size, result);

    for (int i = 0; i < operands_size; i++)
    {
        free(operands_array[i]);
    }

    //Libera memória
    free(a);
    free(b);

    return 0;
}
