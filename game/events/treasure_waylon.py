#Empty py intended as a suggestion for a type of event a student could add. For ease of merging, students should append their names or other id to this py and any classes, to reduce conflicts.

from game import event
import random
import game.config as config
from game.context import Context
from game.player import Player

from game.items import GoldenSword

class Treasure (Context, event.Event):
    '''  '''
    def __init__(self):
        super().__init__()
        self.name = "treasure."
        self.treasureExists = (random.random() < 0.5)
        self.go = False
        self.verbs['dig'] = self
        self.verbs['ignore'] = self
        self.verbs['help'] = self
        self.result = {}

    def process_verb (self, verb, cmd_list, noun):
        if (verb == "dig"):
            if self.treasureExists:
                self.result["message"] = "The crew found a chest with a golden sword!"
                config.the_player.inventory.append(GoldenSword())
                self.go = True
            else:
                self.result["message"] = "The crew didn't find a treasure chest."
                self.go = True

        elif (verb == "ignore"):
            self.result["message"] = "The crew ignored the treasure spot."
            self.go = True

        elif (verb == "help"):
            print ("There might be a treasure chest if you dig at the spot.")
            self.go = False

        else:
            self.go = False
        

    def process(self, world):
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print ("The crew has found a treasure spot. What do you want to do? ")
            Player.get_interaction ([self])

        return self.result