from threading import Lock

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

mutex_oil = Lock()
mutex_uranium = Lock()
mutex_moon_needs = Lock()
mutex_moon_request = Lock()
moon_needs = {
    'fuel': False,
    'uranium': False,
}
moon_request = {
    'request': False,
    'response': False,
}

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
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases
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
