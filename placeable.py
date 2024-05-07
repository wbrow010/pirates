from game.display import announce
import game.items as items
import random
import game.config as config
from game.items import Key

class Placeable:
    def __init__(self, name):
        self.name = name
        self.item = None
        self.requires_key = False
        self.locked = False

        self.prepositions = ["on"] #words like "inside" or "on" or "behind"

    def unlock(self):
        if self.requires_key:
            for item in config.the_player.inventory:
                if isinstance(item, Key):
                    config.the_player.inventory.pop(config.the_player.inventory.index(item))
                    self.locked = False
                    announce(f"You unlock the {self.name} with the key.")
                    return
            announce(f"You don't have a key in your inventory.")
        else:
            announce(f"The {self.name} doesn't need a key.")


    def placeItem(self, item):
        if not self.locked:
            if self.item == None:
                self.item = item
                announce(f"You place the {item.name} on the {self.name}.")
            else:
                config.the_player.inventory.append(self.item)
                announce(f"You pick up the {self.item.name} {self.prepositions[0]} the {self.name} and place the {item.name} down.")
                self.item = item
        else:
            announce(f"The {self.name} is locked.")

    def grabItem(self):
        if not self.locked:
            if self.item != None:
                config.the_player.inventory.append(self.item)
                announce(f"You pick up the {self.item.name} {self.prepositions[0]} the {self.name}.")
                self.item = None
            else:
                announce(f"There is no item {self.prepositions[0]} the {self.name}.")
        else:
            announce(f"The {self.name} is locked.")