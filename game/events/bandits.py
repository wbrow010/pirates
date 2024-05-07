import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
from game.display import announce

class Bandits (event.Event):
    '''
    A combat encounter with a crew of bandits.
    When the event is drawn, creates a combat encounter with 2-4 bandits, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " drowed pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with Drowned monsters. The first Drowned may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the bandits are defeated!"
        monsters = []
        #2-4 bandits
        for i in range (random.randint(2,5)):
            monsters.append(combat.Bandit("Bandit"))

        announce ("You are attacked by a crew of Bandits!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
