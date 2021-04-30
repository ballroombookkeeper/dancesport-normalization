import re
from typing import List

from dancesport_normalization.enums import Dance, Style

_danceCodeToDance = {
    'W': Dance.Waltz,
    'T': Dance.Tango,
    'F': Dance.Foxtrot,
    'V': Dance.VienneseWaltz,
    'Q': Dance.Quickstep,
    'C': Dance.ChaCha,
    'R': Dance.Rumba,
    'B': Dance.Bolero,
    'J': Dance.Jive,
    'H': Dance.Hustle,
    '#': Dance.Showdance,
    '2': Dance.TwoStep
    # Swing/Samba, Mambo/Merengue, Peabody/Paso/Polka overlap - need special logic
}

_danceNameToDance = {
    'waltz': Dance.Waltz,
    'tango': Dance.Tango,
    'foxtrot': Dance.Foxtrot,
    'v waltz': Dance.VienneseWaltz,
    'viennese waltz': Dance.VienneseWaltz, # TODO
    'quickstep': Dance.Quickstep,
    'cha cha': Dance.ChaCha,
    'rumba': Dance.Rumba,
    'swing': Dance.Swing,
    'mambo': Dance.Mambo,
    'bolero': Dance.Bolero,
    'samba': Dance.Samba,
    'jive': Dance.Jive,
    'paso doble': Dance.PasoDoble,
    'hustle': Dance.Hustle,
    'merengue': Dance.Merengue
}

def _getDanceFromCode(code: str, context: str = None) -> Dance:
    upperCode = code.upper()
    if upperCode in _danceCodeToDance:
        return _danceCodeToDance[upperCode]

    return None

def _getDance(input: str) -> Dance:
    """ Gets corresponding Dance from input """
    lowerInput = input.strip().lower().replace('.', '')

    if 'v waltz' in lowerInput or 'viennese waltz' in lowerInput:
        return Dance.VienneseWaltz

    if lowerInput in _danceNameToDance:
        return _danceNameToDance[lowerInput]

    return None

def getDances(input: str) -> List[Dance]:
    """ Gets corresponding Dances from input """
    lowerInput = input.lower().replace('.', '')
    tokens = lowerInput.split(' ')

    lastParenthetical = re.match(r'\((.*)\)', tokens[-1])
    if not lastParenthetical:
        nonCodeResults = _getDance(input)
        if nonCodeResults is None:
            return None
        return [nonCodeResults] # TODO: Weird case
    danceChars = lastParenthetical.group(1)
    numDances = len(danceChars)

    if numDances == 1:
        danceName = tokens[-2]
        potentialViennese = tokens[-3]
        potentialDance = _getDance(danceName)
        if potentialDance == Dance.Waltz and (potentialViennese == 'v' or potentialViennese == 'viennese'):
            return [Dance.VienneseWaltz]
        return [potentialDance]

    dances = [_getDanceFromCode(code) for code in danceChars]
    if None in dances:
        return None

    return dances

def getStyle(input: str) -> Style:
    """ Gets corresponding Style from input """
    return None