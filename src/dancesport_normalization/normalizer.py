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
    'N': Dance.NightclubTwoStep,
    '_': Dance.Other,
    'E': Dance.Other
    # Swing/Samba, Mambo/Merengue, Peabody/Paso/Polka overlap - need special logic
}

_danceCodeInSuperStyleDance = {
    SuperStyle.American: {
        'W': Dance.Waltz,
        'T': Dance.Tango,
        'F': Dance.Foxtrot,
        'V': Dance.VienneseWaltz,
        'P': Dance.Peabody,
        'C': Dance.ChaCha,
        'R': Dance.Rumba,
        'S': Dance.Swing,
        'M': Dance.Mambo,
        'B': Dance.Bolero
    },
    SuperStyle.International: {
        'W': Dance.Waltz,
        'T': Dance.Tango,
        'F': Dance.Foxtrot,
        'V': Dance.VienneseWaltz,
        'Q': Dance.Quickstep,
        'S': Dance.Samba,
        'C': Dance.ChaCha,
        'R': Dance.Rumba,
        'P': Dance.PasoDoble,
        'J': Dance.Jive
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

def _getDanceCodes(eventString: str) -> str:
    lowerInput = eventString.lower().replace('.', '')
    tokens = lowerInput.split(' ')

    # Check for dance codes at end
    lastParenthetical = re.match(r'\((.*)\)', tokens[-1])
    if lastParenthetical:
        return lastParenthetical.group(1)
    return None

def _getDanceFromCode(code: str, superStyle: SuperStyle = None) -> Dance:
    upperCode = code.upper()
    if upperCode in _danceCodeToDance:
        return _danceCodeToDance[upperCode]

    if superStyle is not None and superStyle in _danceCodeInSuperStyleDance and upperCode in _danceCodeInSuperStyleDance[superStyle]:
        return _danceCodeInSuperStyleDance[superStyle][upperCode]

    return None

def _getDance(eventString: str) -> Dance:
    """ Gets corresponding Dance from eventString """
    lowerEventString = eventString.strip().lower().replace('.', '')

    if 'v waltz' in lowerEventString or 'viennese waltz' in lowerEventString:
        return Dance.VienneseWaltz

    if lowerEventString in _danceNameToDance:
        return _danceNameToDance[lowerEventString]

    return None

def getDances(eventString: str) -> List[Dance]:
    """ Gets corresponding Dances from eventString """
    lowerEventString = eventString.lower().replace('.', '')
    tokens = lowerEventString.split(' ')
    danceChars = _getDanceCodes(lowerEventString)

    # Check for dance codes at end
    lastParenthetical = re.match(r'\((.*)\)', tokens[-1])
    if not danceChars:
        nonCodeResults = _getDance(eventString)
        if nonCodeResults is None:
            return None
        return [nonCodeResults] # TODO: Weird case
        
    numDances = len(danceChars)

    superStyle = getSuperStyle(eventString)

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

def getSuperStyle(eventString: str) -> SuperStyle:
    """ Gets corresponding SuperStyle from input """
    lowerEventString = eventString.lower()

    if any([substr in lowerEventString for substr in ['nine dance', '9-dance', '9 dance', 'american', 'am.', 'rhythm', 'smooth']]):
        return SuperStyle.American

    if any([substr in lowerEventString for substr in ['ten dance', '10-dance', '10 dance', 'international', 'intl.', 'standard', 'latin']]):
        return SuperStyle.International

    danceCodes = _getDanceCodes(eventString)

    # This assumes all dances are the same super style - in the case of "Amateur Pre-Teen II Silver Multi-Dance (WFQSCR)" this may not be the case (Quickstep and Swing)
    if danceCodes is not None:
        superStyles = []
        for superStyle in _danceCodeInSuperStyleDance:
            if all([danceCode in _danceCodeInSuperStyleDance[superStyle] for danceCode in danceCodes.upper()]):
                superStyles.append(superStyle)
        if len(superStyles) == 1:
            return superStyles[0]

    return None

def getStyle(eventString: str) -> Style:
    """ Gets corresponding Style from input """
    lowerEventString = eventString.lower().replace('.', '')

    if 'rhythm' in lowerEventString:
        return Style.Rhythm

    if 'smooth' in lowerEventString:
        return Style.Smooth

    if 'standard' in lowerEventString:
        return Style.Standard

    if 'latin' in lowerEventString:
        return Style.Latin

    # TODO: Handle "Am" and "Intl"
    tokens = lowerEventString.split(' ')
    if len(tokens) > 3:
        pass

    return None

def getEventInfo(eventString: str) -> EventInfo:
    name = eventString
    dances = getDances(eventString)
    superStyle = getSuperStyle(eventString)
    style = getStyle(eventString)
    return EventInfo(name, dances, style, superStyle)