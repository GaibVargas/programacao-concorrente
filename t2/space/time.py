
from threading import Thread
from time import sleep

import globals

######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class SimulationTime(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.current_time = 0
    
    def simulation_time(self):
        return self.current_time
    
    def run(self):
        while(globals.get_release_system() == False):
            pass
        
        # Roda enquanto os planetas e bases estiverem ativos
        while(not globals.all_is_done()):
            print(f"{self.current_time} year(s) have passed...")
            self.current_time+=1
            sleep(1)
