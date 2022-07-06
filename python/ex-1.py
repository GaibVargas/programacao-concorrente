from concurrent.futures import ThreadPoolExecutor
from time import sleep
from random import randint
from threading import Semaphore, Lock

def produtor(id):
  global buffer, lock, cheio, vazio
  for i in range(10):
    sleep(randint(0,2))           # fica um tempo produzindo...
    item = 'item ' + str(i)
    vazio.acquire()
    lock.acquire()
    buffer.append(item)
    print('%i Produziu %s (ha %i itens no buffer)' % (id,item,len(buffer)))
    lock.release()
    cheio.release()

def consumidor(id):
  global buffer, lock, cheio, vazio
  for i in range(10):
    cheio.acquire()
    lock.acquire()
    item = buffer.pop(0)
    print('%i Consumiu %s (ha %i itens no buffer)' % (id,item,len(buffer)))
    lock.release()
    vazio.release()
    sleep(randint(0,2))         # fica um tempo consumindo...

buffer = []
tam_buffer = 5
lock = Lock()

cheio = Semaphore(0)
vazio = Semaphore(tam_buffer)

produtores = ThreadPoolExecutor(max_workers=2)
consumidores = ThreadPoolExecutor(max_workers=2)

for i in range(2):
  produtores.submit(produtor, i)
  consumidores.submit(consumidor, i)

produtores.shutdown()
consumidores.shutdown()