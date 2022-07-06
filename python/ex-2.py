from time import sleep
from random import randint
from threading import Semaphore, Thread

def produtor():
  global buffer, lock, cheio, vazio
  for i in range(10):
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i)
    vazio.acquire()
    lock.acquire()
    buffer.append(item)
    print('Produzido %s (ha %i itens no buffer)' % (item,len(buffer)))
    lock.release()
    cheio.release()

def consumidor():
  global buffer, lock, cheio, vazio
  for i in range(10):
    cheio.acquire()
    lock.acquire()
    item = buffer.pop(0)
    print('Consumido %s (ha %i itens no buffer)' % (item,len(buffer)))
    lock.release()
    vazio.release()
    sleep(randint(0,2))         # fica um tempo consumindo...

buffer = []
tam_buffer = 3
lock = Semaphore()

cheio = Semaphore(0)
vazio = Semaphore(tam_buffer)
# cria semáforos
produtor = Thread(target=produtor) 
consumidor = Thread(target=consumidor) 
produtor.start()
consumidor.start()
produtor.join()
consumidor.join() 