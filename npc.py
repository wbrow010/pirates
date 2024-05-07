from game.display import announce
import game.items as items
import random
import game.config as config

PICKPOCKET_AWAKE_CHANCE = 0.35

class NPC:
    def __init__(self, name):
        self.name = name
        self.interaction_string = "I am an NPC."
        self.pickpocket_string  = "Hey!"
        self.inventory = []
        self.awake = True

    def say(self, string):
        announce(f"{self.name} : \"{string}\"")

    def interact(self):
        self.say(self.interaction_string)

    def pickpocket(self):
        # you can only pickpocket if an npc is asleep
        if not self.awake:
            if len(self.inventory) > 0:
                # Pop a random item from the inventory
                if random.random() < PICKPOCKET_AWAKE_CHANCE:
                    self.awake = True
                    announce(f"{self.name} has woken up.")
                    self.say(self.pickpocket_string)
                else:
                    stolen_item = self.inventory.pop(random.randint(0, len(self.inventory) - 1))
                    announce(f"You've pickpocketed a {stolen_item.name}.")
                    return stolen_item
            else:
                self.say(f"{self.name}'s inventory is empty.")
                return None
        else:
            self.say(self.pickpocket_string)
            return None
