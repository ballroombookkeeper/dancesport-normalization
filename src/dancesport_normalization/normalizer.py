from typing import List

from dancesport_normalization.enums import Dance, Style

def getDance(input: str) -> Dance:
    """ Gets corresponding Dance from input """
    lower_input = input.lower().replace('.', '')
    if lower_input.find('waltz') >= 0 and lower_input.find('viennese') < 0:
        return Dance.Waltz

    return None

def getDances(input: str, hint: List[Dance] = None) -> List[Dance]:
    """ Gets corresponding Dances from input """
    return None

def getStyle(input: str) -> Style:
    """ Gets corresponding Style from input """
    return None