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

    Peabody = 'Pb'
    Hustle = 'H'
    
class Style(Enum):
    Smooth = 1
    Standard = 2
    Rhythm = 3
    Latin = 4