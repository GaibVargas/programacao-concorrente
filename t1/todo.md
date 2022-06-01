# ToDo

## buffet
* buffet run

## chef
* chef_run
* chef_put_food
* chef_check_food

ideia: chamar check_food no run, e dentro do check_food, se precisar, chamar put_food

## globals
com certeza vou usar para criar mutexes e semáforos

## student
* student_seat
* student_serve
* student_leave

## worker gate
* look_queue
* remove_student
* look_buffet
* insert_queue_buffet

## Ideias
Um mutex para cada caixa do buffet, para poder mexer na quantidade do meal
Um mutex para número de estudantes que ainda faltam se servir (se mais de um thread for usar isso não sei)
Um semáforo de 2 lugares para cada caixa de alimento (o semáforo só abre espaço quando a fila andar)