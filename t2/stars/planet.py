from threading import Thread
import globals
# Representa o satélite que mede a habitabilidade do alvo
class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    # Detecta uma exmplosão
    def nuke_detected(self):
        before_percentage = self.terraform
        while(before_percentage == self.terraform):
            pass
        print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        # Enquanto ainda não estiver sido terraformado, continua a missão
        while(self.terraform > 0):
            # Semáforo que detecta explosão
            # Faz com que a thread não fique em espera ocupada
            globals.get_nuke_detection_semaphore(self.name.lower()).acquire()
            self.nuke_detected()
        
        # Assim que for terraformado, informa ao sistema global que sua missão de detecção acabou
        globals.decrement_threads_to_wait()