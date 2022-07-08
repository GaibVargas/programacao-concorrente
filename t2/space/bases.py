import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
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
        globals.acquire_moon_request()
        globals.acquire_moon_needs()
        if (self.fuel + 120 <= self.constraints[1]):
            globals.set_moon_needs('fuel', True)
            globals.set_moon_request('request', True)
        if (self.uranium + 75 <= self.constraints[0]):
            globals.set_moon_needs('uranium', True)
            globals.set_moon_request('request', True)
        globals.release_moon_needs()
        globals.release_moon_resquest()
    
    def can_help_moon(self):
        if (self.rockets < self.constraints[2]):
            return True
        return False
    
    def construct_rocket_to_moon(self):
        rocket = Rocket('LION')
        rocket.init_resources()
        self.rockets_to_fuel.insert(0, rocket)
        self.rockets += 1

    def check_moon_needs(self):
        globals.acquire_moon_request()
        if (globals.get_moon_request()['request'] and not globals.get_moon_request()['response']):
            if (self.can_help_moon()):
                globals.set_moon_request('response', True)
                self.construct_rocket_to_moon()
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
    
    def refuel_cargo(self, rocket):
        globals.acquire_moon_needs()
        if globals.get_moon_needs()['fuel']:
            rocket.refuel_cargo(120)
            self.fuel -= 120
        globals.release_moon_needs()
    
    def refuel_uranium_cargo(self, rocket):
        globals.acquire_moon_needs()
        if globals.get_moon_needs()['uranium']:
            rocket.refuel_uranium_cargo(75)
            self.uranium -= 75
        globals.release_moon_needs()

    def fuel_base_rockets(self):
        if (self.rockets == 0):
            return
        fuel_needs = globals.get_fuels_needs()
        for rocket in self.rockets_to_fuel:
            if self.fuel > 0:
                self.refuel_rocket(rocket, fuel_needs[self.name][rocket.name])
            if self.uranium > 0 and rocket.name != 'LION':
                self.refuel_rocket_uranium(rocket, 35)
            if rocket.name == 'LION':
                if self.fuel >= 120 and rocket.fuel_cargo < 120:
                    self.refuel_cargo(rocket)
                if self.uranium >= 75 and rocket.uranium_cargo < 75:
                    self.refuel_uranium_cargo(rocket)
                return

    def check_fuel_cargo(self, rocket):
        if globals.get_moon_needs()['fuel']:
            return rocket.fuel_cargo >= 120
        return True 
    
    def check_uranium_cargo(self, rocket):
        if globals.get_moon_needs()['uranium']:
            return rocket.uranium_cargo >= 75
        return True

    def try_launch_rocket(self):
        fuel_needs = globals.get_fuels_needs()
        rocket_executer = globals.get_rocket_executer()
        for rocket in self.rockets_to_fuel:
            if rocket.name == 'LION':
                if (rocket.fuel >= fuel_needs[self.name][rocket.name] and self.check_fuel_cargo(rocket) and self.check_uranium_cargo(rocket)):
                    rocket_executer.submit(rocket.prepare_to_launch_to_moon, base=self)
                    self.rockets_to_fuel.remove(rocket)
            else:
                if (rocket.fuel >= fuel_needs[self.name][rocket.name] and rocket.uranium >= 35):
                    [must_continue ,target] = self.choose_target()
                    if not must_continue:
                        return False
                    rocket_executer.submit(rocket.prepare_to_launch, base=self, planet=target)
                    self.rockets_to_fuel.remove(rocket)
        return True

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        
        self.rockets_to_fuel = []

        while(True and len(globals.get_target_options()) > 0):
            if (self.name != "MOON"):
                mines = globals.get_mines_ref()
                self.mine_resources(mines)
                self.check_moon_needs()
            else:
                self.request_resources()
            
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
        
        print(f'************************{self.name} TERMINANDO***********************')
        globals.decrement_threads_to_wait()
            