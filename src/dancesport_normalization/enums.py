from enum import Enum

class Dance(Enum):
    Waltz = 'W',
    Tango = 'T',
    Foxtrot = 'F',
    VienneseWaltz = 'V',
    Quickstep = 'Q'

    ChaCha = 'C'
    Rumba = 'R'
    Swing = 'Sw'
    Mambo = 'M'
    Bolero = 'B'
    Samba = 'S'
    Jive = 'J'
    PasoDoble = 'Pd'

    Peabody = 'Pb'
    Hustle = 'H'
    Merengue = 'Me'
    Polka = 'Pk'

    Showdance = '#'
    TwoStep = '2'
    
class Style(Enum):
    Smooth = 1
    Standard = 2
    Rhythm = 3
    Latin = 4

class Level(Enum):
    Newcomer = 1
    Bronze = 2
    Silver = 3
    Gold = 4
    Novice = 5
    Prechamp = 6
    Champion = 7
    RisingStar = 8 # TODO: Does this belong here?
    Professional = 9

class Age(Enum):
    Adult = 1

class Division(Enum):
    Amateur = 1
    ProAm = 2
    Pro = 3