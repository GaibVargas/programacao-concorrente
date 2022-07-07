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

        while(True and self.terraform > 0):
            globals.get_nuke_detection_semaphore(self.name.lower()).acquire()
            self.nuke_detected()
        globals.decrement_threads_to_wait()