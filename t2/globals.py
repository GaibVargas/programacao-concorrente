from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Semaphore

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

# Número de threads envolvidas na missão
# 4 satélites e 4 bases
threads_to_wait = 8

# Controla o acesso à variável acima
mutex_threads_to_wait = Lock()

# Controla o acesso à mina de petróleo
mutex_oil = Lock()

# Controla o acesso à mina de urânio
mutex_uranium = Lock()

# Define os alvos da terraformação
target_options = ['mars', 'io', 'europa', 'ganimedes']

# Controla o acesso à variável acima
mutex_target_options = Lock()

# Controla o acesso aos satélites que monitoram os alvos
targets = {
    'mars': Lock(),
    'io': Lock(),
    'europa': Lock(),
    'ganimedes': Lock()
}

# Controla a quantia de explosões simultâneas no alvo
targets_nuke = {
    'mars': Semaphore(value=2),
    'io': Semaphore(value=2),
    'europa': Semaphore(value=2),
    'ganimedes': Semaphore(value=2)
}

# Controla o bombardeamento dos polos dos alvos
last_target_pole = { # True = North, False = South
    'mars': True,
    'io': True,
    'europa': True,
    'ganimedes': True
}

# Controla o acesso à variável acima
mutex_last_target_pole = {
    'mars': Lock(),
    'io': Lock(),
    'europa': Lock(),
    'ganimedes': Lock()
}

# Controla o acesso dos foguetes às bases de lançamentos
base_launch = {
    'alcantara': Lock(),
    'canaveral cape': Lock(),
    'moscow': Lock(),
    'moon': Lock()
}

# Controla o acesso ao atributo da classe Base que armazena o quantia de foguetes na base
# variável usada nas threads de Base e Rocket
base_rockets_number = {
    'alcantara': Lock(),
    'canaveral cape': Lock(),
    'moscow': Lock(),
    'moon': Lock()
}

# Controla a detecção de explosões no alvo
# O semáforo é aberto por um foguete que alcança seu alvo
# O semáforo é ocupado pelo satélite de monitoramento do alvo
nuke_detection = {
    'mars': Semaphore(value=0),
    'io': Semaphore(value=0),
    'europa': Semaphore(value=0),
    'ganimedes': Semaphore(value=0)
}

# Define a quantia necessária de combustível para um determinado tipo de foguete
# partindo de determinada base
fuel_needs = {
    'ALCANTARA': {
        'DRAGON': 70,
        'FALCON': 100,
        'LION': 100,
    },
    'CANAVERAL CAPE': {
        'DRAGON': 100,
        'FALCON': 120,
        'LION': 115,
    },
    'MOSCOW': {
        'DRAGON': 100,
        'FALCON': 120,
        'LION': 115,
    },
    'MOON': {
        'DRAGON': 50,
        'FALCON': 90,
    }
}

# Variável de controle que informa quais são as necessidades atuais da base luna
moon_needs = {
    'fuel': False,
    'uranium': False,
}

# Controla o acesso à variavel acima
mutex_moon_needs = Lock()

# Variável de controle que informa se há um pedido da Lua, e se já foi atendido
moon_request = {
    'request': False,
    'response': False,
}

# Controla o acesso à variável acima
mutex_moon_request = Lock()

# Executor de threads Rocket
rocket_executer = ThreadPoolExecutor()

# Retorna o pólo viável para bombardeamento e atualiza valor para o pólo contrário
def get_last_target_pole(base):
    global last_target_pole, mutex_last_target_pole
    mutex_last_target_pole[base].acquire()
    last = last_target_pole[base]
    last_target_pole[base] = not last
    mutex_last_target_pole[base].release()
    return last

def get_moon_request():
    global moon_request
    return moon_request

def set_moon_request(key, value):
    global moon_request
    moon_request[key] = value

def set_moon_needs(key, value):
    global moon_needs
    moon_needs[key] = value

def get_moon_needs():
    global moon_needs
    return moon_needs

def get_rocket_executer():
    global rocket_executer
    return rocket_executer

def get_base_rockets_lock(base):
    global base_rockets_number
    return base_rockets_number[base]

def get_base_launch(base):
    global base_launch
    return base_launch[base]

def get_target_nuke_semaphore(target):
    global targets_nuke
    return targets_nuke[target]

def get_thread_wait():
    global threads_to_wait
    return threads_to_wait

# Decremento o número de threads a serem esperadas para o fim do programa
# Decrementados sempre que um planeta já está terraformado ou uma base terminou seu serviço
def decrement_threads_to_wait():
    global threads_to_wait, mutex_threads_to_wait
    mutex_threads_to_wait.acquire()
    threads_to_wait -= 1
    mutex_threads_to_wait.release()

# Retorna se a simulação já acabou
def all_is_done():
    return threads_to_wait == 0

def get_fuels_needs():
    global fuel_needs
    return fuel_needs

def get_nuke_detection_semaphore(planet):
    global nuke_detection
    return nuke_detection[planet]

def acquire_target_options():
    global mutex_target_options
    mutex_target_options.acquire()

def release_target_options():
    global mutex_target_options
    mutex_target_options.release()

def get_target_options():
    global target_options
    return target_options

def remove_target_options(target):
    global target_options
    target_options.remove(target)

def get_target_lock(target):
    global targets
    return targets[target]

def acquire_moon_request():
    global mutex_moon_request
    mutex_moon_request.acquire()

def release_moon_resquest():
    global mutex_moon_request
    mutex_moon_request.release()

def acquire_moon_needs():
    global mutex_moon_needs
    mutex_moon_needs.acquire()

def release_moon_needs():
    global mutex_moon_needs
    mutex_moon_needs.release()

def acquire_oil():
    global mutex_oil
    mutex_oil.acquire()

def release_oil():
    global mutex_oil
    mutex_oil.release()

def acquire_uranium():
    global mutex_uranium
    mutex_uranium.acquire()

def release_uranium():
    global mutex_uranium
    mutex_uranium.release()

def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets, threads_to_wait
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases, threads_to_wait
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

def set_release_system():
    global release_system
    release_system = True

def get_release_system():
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time
