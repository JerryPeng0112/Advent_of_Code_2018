from copy import copy
import re


class Group:
    def __init__(self, army, units, hp, immunity, weakness, dmg, dmgType, \
            initiative):
        self.army = army
        self.units = units
        self.hp = hp
        self.immunity = immunity
        self.weakness = weakness
        self.dmg = dmg
        self.dmgType = dmgType
        self.initiative = initiative
        self.target = -1


    def power(self):
        return self.units * self.dmg


    def toDealDmg(self, defender):
        if self.units <= 0 or self.dmgType in defender.immunity:
            return 0

        dmg = self.power()
        if self.dmgType in defender.weakness:
            dmg *= 2

        return dmg


    def takeDmg(self, attacker):
        dmg = attacker.toDealDmg(self)
        self.units -= (dmg // self.hp)


def main():

    data = readFiles()

    immune, infect = extractArmies(data)

    printArmy(immune, 'Immune System')
    printArmy(infect, 'Infection')

    winner = runSims(immune, infect)

    unitsLeft = calcUnitsLeft(winner)

    print(unitsLeft)


def calcUnitsLeft(winner):
    return sum(map(lambda d: d.units, winner))


def runSims(immune, infect):
    
    while immune and infect:
        immune.sort(key=lambda d: (d.power(), d.initiative), reverse=True)
        infect.sort(key=lambda d: (d.power(), d.initiative), reverse=True)

        selectTarget(infect, immune)
        selectTarget(immune, infect)

        attacking(immune, infect)

        immune = list(filter(lambda d: d.units > 0, immune))
        infect = list(filter(lambda d: d.units > 0, infect))

    printArmy(immune, 'Immune System')
    printArmy(infect, 'Infection')

    winner = None
    if immune:
        winner = immune
    else:
        winner = infect

    return winner


def selectTarget(attackers, defenders):
    defenders = copy(defenders)
    chosen = set()
    for attacker in attackers:

        dmgs = {}
        maxDmg = 0

        # Calculate damage to take for each defender
        for idx, defender in enumerate(defenders):
            if idx not in chosen:
                dmgs[idx] = attacker.toDealDmg(defender)

        if dmgs:
            maxDmg = max(dmgs.values())

        # If unable to deal damage, choose no target
        if maxDmg == 0:
            attacker.target = -1
            continue

        # Get available candidate, sort by effective power and initiative
        cands = { k: defenders[k] for k, v in dmgs.items() if v == maxDmg }
        cands = [ cand for cand in cands.items() ]
        cands.sort(key=lambda d: (d[1].power(), d[1].initiative), \
                reverse=True)

        # Assign a target for attacker
        if cands:
            attacker.target = cands[0][0]
            chosen.add(cands[0][0])

        else:
            attacker.target = -1


def attacking(immune, infect):
    groups = immune + infect
    groups.sort(key=lambda d: d.initiative, reverse=True)

    for group in groups:
        if group.army == 'immune':
            attack(group, infect)
        else:
            attack(group, immune)


def attack(attacker, defenders):
    if attacker.target == -1:
        return

    defender = defenders[attacker.target]
    defender.takeDmg(attacker)


"""
Two armies: immune system, infection
Each army has multiple groups
group: unit, hp, immunity, weakness, dmg, dmg type, initiative

fight consists of 2 phases: target selection and attacking
Effective Power = unit * damage
Target Selection:
    attacker
    in order of: 
        decreasing order of effective power, higher initiative
    choose defender in order of:
        group it would deal most damage, largest effective power, highest initiative
        If it cannot deal damage to any gorups, it does not select a target
        Once the defender selected, remove it from list, 
        attacker select 0 or 1 defender, 
        defenders can get attacked by 0 or 1 attacker

Attack:
    in order of attacker initiative
    deal damage equal to effective power, if immune no dmg, if weak deal double dmg
    Defending group only loses whole unit from dmg

Combat only ends once army lost all units

"""
def printArmy(army, title):
    print(title)
    for d in army:
        print(d.__dict__)
    print()


def extractArmies(data):
    data = data.split('\n')
    splitIdx = data.index('')
    immuneData = data[1: splitIdx]
    infectData = data[splitIdx + 2: -1]

    pattern = re.compile(r'(?P<units>\d+) units each with (?P<hp>\d+) hit points ?'
            r'(?P<props>.*) with an attack that does (?P<attack>.*) damage at '
            r'initiative (?P<initiative>\d+)')
    
    # Fill each army with groups of units
    immune, infect = [], []
    for d in immuneData:
        m = pattern.match(d).groupdict()
        immune.append(createGroup(m, 'immune'))

    for d in infectData:
        m = pattern.match(d).groupdict()
        infect.append(createGroup(m, 'infect'))

    return immune, infect


def createGroup(m, army):
    units = int(m['units'])
    hp = int(m['hp'])
    props = m['props']
    attack = m['attack']
    initiative = int(m['initiative'])

    # Extract dmg and dmgType
    pattern = re.compile(r'(?P<dmg>\d+) (?P<dmgType>.*)')
    attack = pattern.match(attack).groupdict()
    dmg = int(attack['dmg'])
    dmgType = attack['dmgType']

    # Extract immunity and weakness
    props = props[1: -1].split('; ')
    immunity, weakness = [], []

    for prop in props:
        if prop.find('immune') != -1:
            pattern = re.compile(r'immune to (.*)')
            immunity = pattern.match(prop).groups()[0].replace(' ', '').split(',')
        if prop.find('weak') != -1:
            pattern = re.compile(r'weak to (?P<weakness>.*)')
            weakness = pattern.match(prop).groups()[0].replace(' ', '').split(',')

    return Group(army, units, hp, immunity, weakness, dmg, dmgType, initiative)


def readFiles():
    file = open('input.txt', 'r')
    data = file.read()
    file.close()
    return data


if __name__ == '__main__':
    main()
