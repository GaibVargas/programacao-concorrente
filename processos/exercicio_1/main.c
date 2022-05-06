#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>


//       (pai)      
//         |        
//    +----+----+
//    |         |   
// filho_1   filho_2


// ~~~ printfs  ~~~
// pai (ao criar filho): "Processo pai criou %d\n"
//  filhos (ao iniciar): "Processo filho %d criado\n"
//    pai (ao terminar): "Processo pai finalizado!\n"

// Obs:
// - pai deve esperar pelos filhos antes de terminar!


int main(int argc, char** argv) {
    int nchildren = 2;
    int pid;
    for (int i = 0; i < nchildren; i++) {
        pid = fork();
        if (pid == 0) {
            printf("Processo filho %d criado\n", getpid());
            fflush(stdout);
            break;
        } else {
            printf("Processo pai criou %d\n", pid);
            fflush(stdout);
        }
    }

    while (wait(NULL) >= 0);
    if (pid > 0) {
        printf("Processo pai finalizado!\n");
        fflush(stdout);
    }
    return 0;
}
