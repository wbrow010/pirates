
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class Lily_island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Arival_beach(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["church"] = Church(self)
        self.locations["church_inside"] = Church_inside(self)

    def enter (self, ship):
        print ("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Arival_beach(location.SubLocation):
    def __init__(self, m):
        '''init beach'''
        super().__init__(m)
        self.name = 'beach'
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #event chance and events TBD

    def enter(self):
        discription = "You arrive at the beach. Your ship anchors next to another pirate ship at the west side of the island."
        discription = discription + "\n You can see the top of a building in the center of the island."
        announce(discription)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north" or verb == "south"):
            announce ("You walk all around the island on the beach. You notice a building in the center of the island")
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["church"]

class Church(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "church"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        #items and verbs TBD

    def enter(self):
        description = "You walk to the building. It is a weathered building with the front doors hanging off their hinges."
        description = description + "\nYou also spot an enterance to the buildings cellar."
        #posible spawn items
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if (verb == "north" or verb == "south" or verb == "east"):
            announce("We're doing stuff")
        if (verb == "in cellar" or verb == "downstairs"):
            announce("headed downstairs")
            #config.the_player.next_loc = self.main_location.locations["cellar"]
        if (verb == "inside" or verb == "into the church" or verb == "inside church"):
            config.the_player.next_loc = self.main_location.locations["church_inside"]
            #announce("heading inside")

class Church_inside(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "church_inside"
        self.verbs['talk'] = self
        self.verbs['take'] = self
        self.verbs['leave'] = self
        self.verbs['east'] = self
        self.verbs['paper'] = self
        #items and verbs TBD
        self.note = 1
        self.gold = 1

    def enter(self):
        description = "You walk through the broken doors and enter what used to be a church. The room is lit by light streaming in through the large holes in the roof."
        description = description + "\nAs you enter you spot a person in tattered robes sitting on a rotting pew with their back facing you. They say nothing."
        description = description + "\nYou also spot the shine of gold on the puplit on the other side of the room."
        announce(description)
        #posible spawn items

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "east" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["church"]
        if (verb == "talk"):
            announce("As you approch the person you realize this person has been dead a long time. They are cluching a peice of paper in their hand.")
        if (verb == "in cellar" or verb == "downstairs"):
            announce("headed downstairs")
            #config.the_player.next_loc = self.main_location.locations["cellar"]

        if verb == "take":
            if self.note == None and self.gold == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.note
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the corpse.")
                    config.the_player.add_to_inventory([item])
                    self.note = None
                    #moves time forward
                    config.the_player.go = True
                    at_least_one = True
                item = self.gold
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up a "+item.name+" plate from the pulpit. It has strange writing on it")
                    config.the_player.add_to_inventory([item])
                    self.gold = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")

