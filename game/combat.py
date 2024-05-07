import random
import game.config as config
import game.crewmate as crew
import game.superclasses as superclasses
from game.context import Context
from game.display import announce
from game.display import menu

import game.items as items

class Combat():

    def __init__ (self, monsters):
        self.monsters = monsters

    def process_verb (self, verb, cmd_list, nouns):
        print (self.nouns + " can't " + verb)

    def crewmateAction(self, attacker, allies, enemies):
        """The player chooses an action for a crewmate to take."""
        announce(attacker.get_name() + " has seized the initiative! What should they do?",pause=False)
        actions = attacker.getAttacks()
        # actions = attacker.getMiscActions()
        if len(actions) > 0:
            choice = menu (actions)
            return actions[choice]
        #else: run in circles, scream and shout
        return None

    def combat (self):
        while len(self.monsters):
            combatants = config.the_player.get_pirates() + self.monsters
            min_t = None
            for c in combatants:
                t = (100 - c.cur_move)/c.speed
                if min_t == None:
                    min_t = t
                else:
                    min_t = min(t, min_t)
            for c in combatants:
                c.cur_move += c.speed*min_t
            speeds = [c.cur_move for c in combatants]
            max_move = max(speeds)
            ready = [c for c in combatants if c.cur_move == max_move]
            moving = random.choice(ready)
            moving.cur_move = 0
            if isinstance(moving, crew.CrewMate):
                chosen_action = self.crewmateAction(moving, config.the_player.get_pirates(), self.monsters)
                if(chosen_action != None):
                    chosen_targets = chosen_action.pickTargets(chosen_action, moving, config.the_player.get_pirates(), self.monsters)
            else:
                chosen_targets = [random.choice(config.the_player.get_pirates())]
                chosen_action = moving.pickAction()
            #Resolve
            chosen_action.resolve(chosen_action, moving, chosen_targets)
            self.monsters = [m for m in self.monsters if m.health >0]
            config.the_player.cleanup_items()


class Monster(superclasses.CombatCritter):
    def __init__ (self, name: str, hp: int, attacks: dict[str, list], speed: float):
        super().__init__(name, hp, speed)
        self.attacks = attacks
        self.cur_move = 0

    def getAttacks(self):
        attacks = []
        for key in self.attacks.keys():
            attack = superclasses.Attack(key, self.attacks[key][0], self.attacks[key][1], self.attacks[key][2], False)
            attacks.append(superclasses.CombatAction(attack.name, attack, self))
        return attacks
    
    def getCombatAction(self, name):
        return superclasses.CombatAction(name, superclasses.Attack(name, self.attacks[name][0], self.attacks[name][1], self.attacks[name][2], False), self)


    def pickAction(self):
        attacks = self.getAttacks()
        return random.choice(attacks)

class Macaque(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))

class Drowned(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (5,15)]
        attacks["punch 1"] = ["punches",random.randrange(35,51), (1,10)]
        attacks["punch 2"] = ["punches",random.randrange(35,51), (1,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))

class Skeleton(Monster):
    def __init__(self, name):
        attacks = {}
        #slash with sword, 50%-75% chance, 10-15 damage
        attacks["slash"] = ["slashes", random.randrange(50,76), (10,15)]
        #stab with sword, 75%-100% chance, 6-11 damage
        attacks["stab"] = ["stabs", random.randrange(75,101), (6,11)]

        super().__init__(name, random.randrange(15,25), attacks, 50 + random.randrange(-15,10))

    def pickAction(self):
        if self.health < 8: #if health is low, resort to a weaker, but more reliable attack
            return self.getCombatAction("stab")
        else:
            return self.getCombatAction("slash")
        
    def on_death (self):
        bone_drops = random.randint(1,2) #number of bones to drop
        #add bones to inventory
        for i in range(bone_drops):
            config.the_player.inventory.append(items.Bone())
        announce(f"{self.name} dropped {i} bone(s)")

class SkeletonArcher(Monster):
    def __init__(self, name):
        attacks = {}
        #slash with sword, 50%-75% chance, 10-15 damage
        attacks["shoot"] = ["shoots", random.randrange(15,30), (15,25)]

        super().__init__(name, random.randrange(8,16), attacks, 150 + random.randrange(-30,10))

    def on_death (self):
        bone_drops = random.randint(1,2) #number of bones to drop
        #add bones to inventory
        for i in range(bone_drops):
            config.the_player.inventory.append(items.Bone())
        announce(f"{self.name} dropped {i} bone(s)")
    
class Bandit(Monster):
    def __init__(self, name):
        self.inventory = []
        self.swipe_chance = 0.25
        attacks = {}
        attacks["slash"] = ["slashes", random.randrange(15,30), (15,25)]
        attacks["swipe"] = ["swipes", random.randrange(25,45), (5,10)]

        super().__init__(name, random.randrange(8,16), attacks, 150 + random.randrange(-30,10))

    def pickAction(self):
        if random.random() <= self.swipe_chance:
            if len(config.the_player.inventory) > 0:
                stolen_item = config.the_player.inventory.pop(random.randint(0, len(config.the_player.inventory) - 1))
                self.inventory.append(stolen_item)
                announce(f"{self.name} has stolen {stolen_item.name} from you!")

            return self.getCombatAction("swipe")
        
        return self.getCombatAction("slash")

    def on_death (self):
        #return stolen items to inventory
        for item in self.inventory:
            config.the_player.inventory.append(item)
            announce(f"{self.name} dropped {item.name}.")