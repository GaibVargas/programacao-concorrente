from random import randrange, random
from time import sleep
import globals

class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0
            
    # Abastece o foguete com combustível
    def refuel(self, value):
        self.fuel += value
    
    # Abastece o foguete com urânio
    def refuel_uranium(self, value):
        self.uranium += value
    
    # Inicia os recursos do foguete
    # Artifício usado para contornar a impossibilidade de alterar o construtor da classe
    def init_resources(self):
        self.fuel = 0
        self.uranium = 0

    # Abastece a carga de combustível do foguete
    def refuel_cargo(self, value):
        self.fuel_cargo += value
    
    # Abastece a carga de urânio do foguete
    def refuel_uranium_cargo(self, value):
        self.uranium_cargo += value
    
    # Inicia processo de lançamento do foguete para a Lua
    def prepare_to_launch_to_moon(self, base):
        # Tenta usar a base de lançamentos
        if globals.all_is_done():
            return
        # Se apossa da base de lançamentos
        globals.get_base_launch(base.name.lower()).acquire()
        globals.get_base_rockets_lock(base.name.lower()).acquire()
        base.rockets -= 1
        globals.get_base_rockets_lock(base.name.lower()).release()
        globals.get_base_launch(base.name.lower()).release()
        # Lança o foguete
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            sleep(0.01)
            if (random() < 0.05):
                self.general_failure()
            else: # Se houver sucesso durante a viagem, pousa na lua
                self.land_on_moon()

        # Informa ao sistema que os recursos pedidos pela lua foram atendidos
        # No caso de falha no lançamento ou na viagem, um novo pedido será aberto pela base lunar
        globals.acquire_moon_request()
        globals.set_moon_request('response', False)
        globals.set_moon_request('request', False)
        globals.acquire_moon_needs()
        globals.set_moon_needs('fuel', False)
        globals.set_moon_needs('uranium', False)
        globals.release_moon_needs()
        globals.release_moon_resquest()

    # Reabastece a base lunar
    def land_on_moon(self):
        moon = globals.get_bases_ref()['moon']
        moon.fuel += self.fuel_cargo
        moon.uranium += self.uranium_cargo
        print(f"\n\n\n\n[TRANSPORT] - The {self.name} {self.id} ROCKET reached the MOON\n\n\n\n")
    
    # Inicia processo de lançamento do foguete a um alvo de terraformação
    def prepare_to_launch(self, base, planet, pole):
        if globals.all_is_done():
            return
        # Define o polo a ser atingido
        if pole:
            self.pole = 'North'
        else:
            self.pole = 'South'
        
        # Verifica se o planeta já não está sendo bombardeado por 2 foguetes
        # Há um timeout, caso haja dois foguetes, não é necessário esperar que eles atinjam o planeta
        # O tempo de viagem é superior ao tempo de espera, logo não haverá mais de 2 impactos simultâneos
        acquire_nuked_planet = globals.get_target_nuke_semaphore(planet.name.lower()).acquire(timeout=0.5)
        # Se apossa da base de lançamentos
        globals.get_base_launch(base.name.lower()).acquire()
        globals.get_base_rockets_lock(base.name.lower()).acquire()
        base.rockets -= 1
        globals.get_base_rockets_lock(base.name.lower()).release()
        globals.get_base_launch(base.name.lower()).release()
        # Realiza o lançamento
        self.launch(base, planet)
        if acquire_nuked_planet:
            globals.get_target_nuke_semaphore(planet.name.lower()).release()
 
    # Aplica dano da explosão no alvo, e sinaliza ao sensor que houve explosão
    def nuke(self, planet): # Permitida a alteração
        target = globals.get_target_lock(planet.name.lower())
        target.acquire()
        planet.terraform -= self.damage()
        target.release()
        globals.get_nuke_detection_semaphore(planet.name.lower()).release()
        print(f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on {self.pole} Pole")
    
    def voyage(self, planet): # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.
        self.simulation_time_voyage(planet)
        failure =  self.do_we_have_a_problem()
        # Se não houver falhas durante a viagem, bombardeia o alvo
        if not failure:
            self.nuke(planet)


    ####################################################
    #                   ATENÇÃO                        # 
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################
    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            sleep(2) # Marte tem uma distância aproximada de dois anos do planeta Terra.
        else:
            sleep(5) # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False
            
    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")
    
    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True
    
    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)        
