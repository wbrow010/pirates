from game import location
import game.config as config
from game.display import announce
from npc import NPC
from placeable import Placeable
from game.items import Key
from game.items import Orb
from game.items import PocketLint
from game.items import DoubleBarrelFlintlock
import game.config as config
from game.events import *

class IslandCave(location.Location):
    
    def __init__(self,x,y,w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'O'
        self.visitable = True
        self.starting_location = BeachSouth(self)
        #         [D][T]
        #         [C]
        # [T]<-[B][B][V]->[S]/[B]
        #         [B]
        #
        self.locations = {}
        self.locations["beachSouth"]   = self.starting_location
        self.locations["beachWest"]    = BeachWest(self)
        self.locations["beachWestTrees"]    = BeachWestTrees(self)
        self.locations["beachNorth"]   = BeachNorth(self)
        self.locations["caveEntrance"] = CaveEntrance(self)
        self.locations["caveDoor"]     = CaveDoor(self)
        self.locations["caveTreasure"] = CaveTreasure(self)

        self.locations["beachVillage"] = BeachVillage(self)
        self.locations["villageBar"]   = VillageBar(self)
        self.locations["villageShop"]  = VillageShop(self)

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class BeachSouth(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        announce("You arrive at the beach. Your ship is at anchor on a wooden dock to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["beachNorth"]
        elif (verb == "east" or verb == "west" or verb == "south"):
            announce (f"You try to walk {verb}, but are stopped by the shoreline")


class BeachNorth(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        announce("You arrive at the center of the island. The elevation is the highest here, and you can see a village to the east, and a cove to the north.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["caveEntrance"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["beachVillage"]
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beachSouth"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beachWest"]

class BeachWest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['east'] = self
        self.verbs['trees'] = self
        
    def enter(self):
        announce("You arrive at the west end of the island. Three trees create a triangle nearby.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["beachNorth"]
        if (verb == "trees"):
            config.the_player.next_loc = self.main_location.locations["beachWestTrees"]
        else:
            announce (f"You try to walk {verb}, but are stopped by the shoreline")

class BeachWestTrees(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['exit'] = self

        self.placeables = [SmallBox()]
        
    def enter(self):
        announce("You walk inbetween the three trees. In the middle of the trees, the top of a small wood box can be seen under the sand.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit"):
            config.the_player.next_loc = self.main_location.locations["beachWest"]
        else:
            announce (f"You try to walk {verb}, but are stopped by the shoreline")

class BeachVillage(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "village"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['bar'] = self
        self.verbs['shop'] = self

    def enter(self):
        announce("You arrive at a village on the beach. There is a bar, a shop, and multiple houses")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beachNorth"]
        if (verb == "bar"):
            config.the_player.next_loc = self.main_location.locations["villageBar"]
        if (verb == "shop"):
            config.the_player.next_loc = self.main_location.locations["villageShop"]
        elif (verb == "north" or verb == "east" or verb == "south"):
            announce (f"You try to walk {verb}, but are stopped by the shoreline")


class CaveEntrance(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        announce("You arrive at a cove. The center of the island is south. There is an entrance to a cave to the north.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["beachNorth"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["caveDoor"]
        else:
            announce (f"You try to walk {verb}, but are stopped by the shoreline")

class CaveDoor(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.placeables = [Pedestal()]

        self.pedestal = self.placeables[0]

        #chance of bandits by the cave door
        self.event_chance = 25
        self.events.append(bandits.Bandits())

    def enter(self):
        announce("You enter a bend in the cave, with a door to the east and the exit to the south.")
        if self.pedestal.item == None:
            announce("There is a pedestal with a spot for a small orb carved out.")
        else:
            announce(f"There is a pedestal with a {self.pedestal.item.name} on top of it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            if self.pedestal.item != None:
                if self.pedestal.item.name == "orb":
                    config.the_player.next_loc = self.main_location.locations["caveTreasure"]
                else:
                    announce("The door is still locked. Perhaps the wrong item is on the pedestal...")
            else:
                print("The door is still locked. It looks like the pedestal needs an item on it...")
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["caveEntrance"]
        else:
            announce (f"You try to walk {verb}, but the cave walls stop you.")

class CaveTreasure(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        #skeletons always spawn in treasure room
        self.event_chance = 100
        self.events.append(skeletons.Skeletons())

        self.placeables = [GoldenChest()]

    def enter(self):
        announce("You walk through the cave door and see a room with a row of stone pillars. At the end of the room lays a golden chest.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["caveDoor"]
        elif (verb == "north" or verb == "west" or verb == "south"):
            announce (f"You try to walk {verb}, but the cave walls stop you.")

class VillageBar(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "bar"
        self.verbs['exit'] = self

        self.npcs = [Bartender(), Man()]

    def enter(self):
        announce("You enter the village's bar. The bartender stands at the counter. A man in the corner stares at you.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit"):
            config.the_player.next_loc = self.main_location.locations["beachVillage"]

class VillageShop(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "shop"
        self.verbs['exit'] = self
        self.verbs['box'] = self
        self.box_item = True

        self.npcs = [Shopkeeper()]
        self.placeables = [Box()]

    def enter(self):
        announce("You enter the village's shop. The shopkeeper is asleep at his desk. A locked box on a shelf has the tag (5000 Shillings) on it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit"):
            config.the_player.next_loc = self.main_location.locations["beachVillage"]
            #check if the player's inventory has a key, remove it, and add the boxes' item to the player's inventory.
            pass

class Bartender(NPC):
    def __init__(self):
        super().__init__("bartender")
        self.interaction_string = "The shopkeeper has a medallion that unlocks a treasure on the island.\nHe keeps in locked in a box in his shop.\nHe keeps the key on him at all times, but I've heard he's hid a spare key somewhere on the island"

class Shopkeeper(NPC):
    def __init__(self):
        super().__init__("shopkeeper")
        self.interaction_string = "ZZZ..."
        self.awake = False
        self.inventory = [Key(), PocketLint()]

class Man(NPC):
    def __init__(self):
        super().__init__("man")
        self.interaction_string = "The shopkeeper hides his key on the west end of the island, but you didn't hear that from me..."

class Pedestal(Placeable):
    def __init__(self):
        super().__init__("pedestal")

class Box(Placeable):
    def __init__(self):
        super().__init__("box")
        self.locked = True
        self.requires_key = True
        self.prepositions = ["in","inside"]
        self.item = Orb()

class SmallBox(Placeable):
    def __init__(self):
        super().__init__("box")
        self.prepositions = ["in","inside"]
        self.item = Key()

class GoldenChest(Placeable):
    def __init__(self):
        super().__init__("chest")
        self.prepositions = ["in","inside"]
        self.item = DoubleBarrelFlintlock()