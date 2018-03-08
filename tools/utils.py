import dateutil
from functools import partial

HIGHLIGHT = "darkgreen"
HIGHLIGHT2 = "#32CD32"

def unquote(value):
    if value and value.startswith('"'):
        value = value[1:-1]
    return value


def parsetime(time):
    time = unquote(time)
    if time and time.startswith("T"):
        return int(time[1:])
    try:
        return dateutil.parser.parse(time) if time else None
    except:
        return None
