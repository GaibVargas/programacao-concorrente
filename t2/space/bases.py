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
    
    def base_rocket_resources(self, rocket_name): # sinceramente, parece inútil
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
        globals.release_oil()

    def refuel_uranium(self, mine):
        uranium_unities_to_minered = 10
        if (self.uranium + uranium_unities_to_minered > self.constraints[0]):
            return
        globals.acquire_uranium()
        if (mine.unities >= uranium_unities_to_minered):
            mine.unities -= uranium_unities_to_minered
            self.uranium += uranium_unities_to_minered
        globals.release_uranium()   

    def mine_resources(self, mines):
        self.refuel_oil(mines['oil_earth'])
        self.refuel_uranium(mines['uranium_earth'])
    
    def request_resources(self):
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
        rocket = Rocket(model)
        rocket.init_resources()
        self.rockets_to_fuel.append(rocket)
        self.rockets += 1
    
    def choose_target(self):
        while True:
            globals.acquire_target_options()
            target_options = globals.get_target_options()

            if len(target_options) == 0:
                globals.release_target_options()
                return [False, None]
            
            target_option = choice(target_options)
            target_lock = globals.get_target_lock(target_option)
            target = globals.get_planets_ref()[target_option]
            target_lock.acquire()

            if (target.terraform <= 0):
                globals.remove_target_options(target_option)
                target_lock.release()
                globals.release_target_options()
            else:
                target_lock.release()
                globals.release_target_options()
                return [True, target]
    
    def refuel_rocket(self, rocket, fuel_need):
        rocket_need = fuel_need - rocket.fuel
        if self.fuel >= rocket_need:
            rocket.refuel(rocket_need)
            self.fuel -= rocket_need

    def refuel_rocket_uranium(self, rocket, need):
        uranium_needed = need - rocket.uranium
        if self.uranium >= uranium_needed:
            self.uranium -= uranium_needed
            rocket.refuel_uranium(uranium_needed)

    def fuel_base_rockets(self):
        if (self.rockets == 0):
            return
        fuel_needs = globals.get_fuels_needs()
        for rocket in self.rockets_to_fuel:
            if rocket.name != 'LION':
                if self.fuel > 0:
                    self.refuel_rocket(rocket, fuel_needs[self.name][rocket.name])
                if self.uranium > 0:
                    self.refuel_rocket_uranium(rocket, 35)

    def try_launch_rocket(self):
        fuel_needs = globals.get_fuels_needs()
        for rocket in self.rockets_to_fuel:
            if (rocket.fuel >= fuel_needs[self.name][rocket.name] and rocket.uranium >= 35):
                [must_continue ,target] = self.choose_target()
                if not must_continue:
                    return False
                rocket_thread = Thread(target=rocket.prepare_to_launch, args=(self, target))
                rocket_thread.start()
                self.rockets_to_fuel.remove(rocket)
                return True
        return True

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        self.rockets_to_fuel = []
        self.launched_rockets = []

        while(True and len(globals.get_target_options()) > 0):
            mines = globals.get_mines_ref()
            if (self.name != "MOON"):
                self.mine_resources(mines)
                # self.check_moon_needs() continua no final
                if (self.rockets < self.constraints[2]):
                    self.construct_new_rocket()
                if (self.rockets > 0):
                    self.fuel_base_rockets()
                must_continue = self.try_launch_rocket()
                if not must_continue:
                    break
                globals.acquire_print()
                self.print_space_base_info()
                globals.release_print()
            else:
                break
            #     self.request_resources()
        
        print(f'************************{self.name} TERMINANDO***********************')
        globals.decrement_threads_to_wait()
            