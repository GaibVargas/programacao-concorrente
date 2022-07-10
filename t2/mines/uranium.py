from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        print(f"🔨 - [{self.location}] - {self.unities} uranium unities are produced.")

    def produce(self):
        globals.acquire_uranium()
        if(self.unities < self.constraint):
            self.unities+=15
            self.print_store_house()
        globals.release_uranium()
        sleep(0.001)
        

    def run(self):
        globals.acquire_print()
        self.print_store_house()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
        # Aprimorei a cláusula para não rodar para sempre
        while(not globals.all_is_done()):
            self.produce()