from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Fish(Context, event.Event):
    '''Encounter where the crew can catch fish and add food to the ship. 
    Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "fish spotted"
        self.verbs['catch'] = self
        self.verbs['ignore'] = self
        self.result = {}
        self.go = False
        self.num_fish = int()

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "catch"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.num_fish = r 
                self.result["message"] = f"You were able to catch {self.num_fish}."
                 #config.the_player.ship.food += n_appearing*3
                config.the_player.ship.food += 5*self.num_fish
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.num_fish = r*3                    
                    self.result["message"] = c. get_name() + f"was lucky and caught {self.num_fish}."
                    config.the_player.ship.food += 5*self.num_fish
                else:
                    self.num_fish = r 
                    self.result["message"] = f"You were able to catch {self.num_fish}."
                    #config.the_player.ship.food += n_appearing*3
                    config.the_player.ship.food += 5*self.num_fish

        elif (verb == "ignore"):
            self.result["message"] = "You decide it's best to sail onwards."
            self.go = True
        else:
            print ("it seems the only options here are to catch or ignore")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print ("You spot many fish in the water here, what do you want to do?")
            Player.get_interaction ([self])

        return self.result
