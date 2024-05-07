import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Skeletons (event.Event):
    '''
    A combat encounter with a crew of skeletons.
    When the event is drawn, creates a combat encounter with 3-5 skeletons, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " drowed pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with Skeleton and Skeleton Archers.'''
        result = {}
        result["message"] = "the skeletons are defeated!"
        monsters = []
        #2-3 skeletons
        for i in range (random.randint(1,3)):
            monsters.append(combat.Skeleton("Skeleton"))

        #1-2 skeleton archers
        for i in range (random.randint(1,2)):
            monsters.append(combat.SkeletonArcher("Skeleton Archer"))

        announce ("You are attacked by a crew of Skeletons!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
