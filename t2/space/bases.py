import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, uranium, fuel, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")
    
    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")

    def refuel_oil(self, mine):
        fuel_unities_to_minered = 10
        if (self.fuel + fuel_unities_to_minered > self.constraints[1]):
            return
        globals.acquire_oil()
        if (mine.unities >= fuel_unities_to_minered):
            mine.unities -= fuel_unities_to_minered
            self.fuel += fuel_unities_to_minered
            print(f"[{self.name}] Pegando combustível de {mine.location}")
        globals.release_oil()

    def refuel_uranium(self, mine):
        uranium_unities_to_minered = 10
        if (self.uranium + uranium_unities_to_minered > self.constraints[0]):
            return
        globals.acquire_uranium()
        if (mine.unities >= uranium_unities_to_minered):
            mine.unities -= uranium_unities_to_minered
            self.uranium += uranium_unities_to_minered
            print(f"[{self.name}] Pegando urânio de {mine.location}")
        globals.release_uranium()   

    def mine_resources(self, mines):
        self.refuel_oil(mines['oil_earth'])
        self.refuel_uranium(mines['uranium_earth'])
    
    def request_resources(self):
        print("Lua pedindo arrego")
        if (self.fuel < 50):
            globals.acquire_moon_needs()
            globals.moon_needs['fuel'] = True

            globals.acquire_moon_request()
            globals.moon_request['request'] = True
            globals.release_moon_resquest()

            globals.release_moon_needs()
        if (self.uranium <= 35 or self.uranium + 75 <= self.constraints[0]):
            globals.acquire_moon_needs()
            globals.moon_needs['uranium'] = True

            globals.acquire_moon_request()
            globals.moon_request['request'] = True
            globals.release_moon_resquest()

            globals.release_moon_needs()
    
    def can_help_moon(self):
        if (self.rockets < self.constraints[2]):
            return True
        return False

    def check_moon_needs(self):
        globals.acquire_moon_request()
        if (globals.moon_request['request'] and not globals.moon_request['response']):
            if (self.can_help_moon()):
                globals.moon_request['response'] = True

        globals.release_moon_resquest()

    def construct_new_rocket(self):
        options = ['DRAGON', 'FALCON']
        model = choice(options)
        target_options = ['mars', 'io', 'europa', 'ganimedes']
        target = choice(target_options)
        self.rockets_on_base.append(Rocket(model))
        self.targets.append(globals.get_planets_ref()[target])
        self.rockets += 1
    
    def fuel_base_rockets(self):
        if (self.rockets == 0):
            return
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
        for index, rocket in enumerate(self.rockets_on_base):
            if rocket.name != 'LION':
                if (self.fuel >= fuel_needs[self.name][rocket.name] and self.uranium >= 35):
                    self.fuel -= fuel_needs[self.name][rocket.name]
                    self.uranium -= 35
                    rocket.launch(self, self.targets[index])
                    self.rockets_on_base.remove(rocket)
                    self.targets.pop(index)
                    self.rockets -= 1
                    return

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        self.rockets_on_base = []
        self.targets = []

        while(True):
            mines = globals.get_mines_ref()
            if (self.name != "MOON"):
                self.mine_resources(mines)
                # self.check_moon_needs() continua no final
                if (self.rockets < self.constraints[2]):
                    self.construct_new_rocket()
                self.fuel_base_rockets()
                globals.acquire_print()
                print(self.rockets_on_base)
                self.print_space_base_info()
                globals.release_print()
            # else:
            #     self.request_resources()
            