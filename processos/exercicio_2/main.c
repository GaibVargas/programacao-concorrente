#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>


//                          (principal)
//                               |
//              +----------------+--------------+
//              |                               |
//           filho_1                         filho_2
//              |                               |
//    +---------+-----------+          +--------+--------+
//    |         |           |          |        |        |
// neto_1_1  neto_1_2  neto_1_3     neto_2_1 neto_2_2 neto_2_3

// ~~~ printfs  ~~~
//      principal (ao finalizar): "Processo principal %d finalizado\n"
// filhos e netos (ao finalizar): "Processo %d finalizado\n"
//    filhos e netos (ao inciar): "Processo %d, filho de %d\n"

// Obs:
// - netos devem esperar 5 segundos antes de imprmir a mensagem de finalizado (e terminar)
// - pais devem esperar pelos seu descendentes diretos antes de terminar

int main(int argc, char** argv) {
    int nchildren = 2;
    int ngrandchildren = 3;
    int isgrandchildren = 0;
    int pid;
    for (int i = 0; i < nchildren; i++) {
        pid = fork();
        if (pid == 0) {
            printf("Processo %d, filho de %d\n", getpid(), getppid());
            fflush(stdout);

            for (int j = 0; j < ngrandchildren; j++) {
                if (fork() == 0) {
                    printf("Processo %d, filho de %d\n", getpid(), getppid());
                    fflush(stdout);
                    isgrandchildren = 1;
                    break;
                }
            }

            break;
        }
    }

    while (wait(NULL) >= 0);
    if (pid > 0) {
        printf("Processo principal %d finalizado!\n", getpid());
        fflush(stdout);
    } else {
        while(wait(NULL) >= 0);
        if (isgrandchildren) sleep(5);
        printf("Processo %d finalizado\n", getpid());
        fflush(stdout);
    }
    return 0;
}
