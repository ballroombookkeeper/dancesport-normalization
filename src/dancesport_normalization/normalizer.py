import re
from collections import namedtuple
from typing import List

from dancesport_normalization.enums import Dance, Style, SuperStyle

EventInfo = namedtuple('EventInfo', ['name', 'dances', 'style', 'superStyle'])

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
    '2': Dance.TwoStep,
    '_': Dance.Other
    # Swing/Samba, Mambo/Merengue, Peabody/Paso/Polka overlap - need special logic
}

_danceCodeInStyleDance = {
    Style.Rhythm: {
        'S': Dance.Swing,
        'M': Dance.Mambo,
        'B': Dance.Bolero
    },
    Style.Smooth: {
        'P': Dance.Peabody
    },
    Style.Latin: {
        'P': Dance.PasoDoble,
        'S': Dance.Samba
    },
    Style.Standard: {

    }
}

_danceCodeInSuperStyleDance = {
    SuperStyle.American: {
        'S': Dance.Swing,
        'M': Dance.Mambo,
        'B': Dance.Bolero,
        'P': Dance.Peabody
    },
    SuperStyle.International: {
        'P': Dance.PasoDoble,
        'S': Dance.Samba
    }
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

def _getDanceFromCode(code: str, superStyle: SuperStyle = None) -> Dance:
    upperCode = code.upper()
    if upperCode in _danceCodeToDance:
        return _danceCodeToDance[upperCode]

    if superStyle is not None and superStyle in _danceCodeInSuperStyleDance and upperCode in _danceCodeInSuperStyleDance[superStyle]:
        return _danceCodeInSuperStyleDance[superStyle][upperCode]

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

    # Check for dance codes at end
    lastParenthetical = re.match(r'\((.*)\)', tokens[-1])
    if not lastParenthetical:
        nonCodeResults = _getDance(input)
        if nonCodeResults is None:
            return None
        return [nonCodeResults] # TODO: Weird case
    danceChars = lastParenthetical.group(1)
    numDances = len(danceChars)

    superStyle = getSuperStyle(input)

    # If only one dance code, attempt to get dance from code, else part it from event name
    if numDances == 1 and len(tokens) >= 3:
        dance = _getDanceFromCode(danceChars, superStyle)
        if dance is not None:
            return [dance]

        danceName = tokens[-2]
        potentialViennese = tokens[-3]
        potentialDance = _getDance(danceName)
        if potentialDance == Dance.Waltz and (potentialViennese == 'v' or potentialViennese == 'viennese'):
            return [Dance.VienneseWaltz]
        return [potentialDance]

    # Get dances from codes
    dances = [_getDanceFromCode(code, superStyle) for code in danceChars]
    if None in dances:
        return None

    return dances

def getSuperStyle(input: str) -> SuperStyle:
    """ Gets corresponding SuperStyle from input """
    lowerInput = input.lower()

    if any([substr in lowerInput for substr in ['nine dance', 'american', 'am.', 'rhythm', 'smooth']]):
        return SuperStyle.American

    if any([substr in lowerInput for substr in ['ten dance', 'international', 'intl.', 'standard', 'latin']]):
        return SuperStyle.International

    return None

def getStyle(input: str) -> Style:
    """ Gets corresponding Style from input """
    lowerInput = input.lower().replace('.', '')

    if 'rhythm' in lowerInput:
        return Style.Rhythm

    if 'smooth' in lowerInput:
        return Style.Smooth

    if 'standard' in lowerInput:
        return Style.Standard

    if 'latin' in lowerInput:
        return Style.Latin

    # TODO: Handle "Am" and "Intl"
    tokens = lowerInput.split(' ')
    if len(tokens) > 3:
        pass

    return None

def getEventInfo(input: str) -> EventInfo:
    name = input
    dances = getDances(input)
    superStyle = getSuperStyle(input)
    style = getStyle(input)
    return EventInfo(name, dances, style, superStyle)