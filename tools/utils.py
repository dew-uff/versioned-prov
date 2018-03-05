import dateutil
from functools import partial

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


def glabeldict(label):
    if label:
        return {
            "labelfontsize": "8",
            "labeldistance": "1.5",
            "color": "darkgreen",
            "labelangle": "60.0",
            "rotation": "20",
            "label": label
        }
    return {}


def labeldict(label):
    if label:
        return {
            "labelfontsize": "8",
            "labeldistance": "1.5",
            "labelangle": "60.0",
            "rotation": "20",
            "taillabel": label
        }
    return {}


def arrow2(dot, first, second, label="", extra={}, labeldict=labeldict):
    if not first or not second:
        return None

    url1 = dot.prefix(first)
    url2 = dot.prefix(second)

    return dot.arrow(url1, url2, attrs=dict(**labeldict(label), **extra))


def arrow3(dot, source, target1, target2, label, extra={}, labeldict=labeldict, attrs={}):
    if sum(1 for x in [source, target1, target2] if x) <= 1:
        return None

    if target1 and target2:
        point, result = dot.point()

        if source:
            surl = dot.prefix(source)
            result += "\n" + dot.arrow(surl, point, attrs=dict(**{
                "arrowhead": "none",
            }, **extra, **attrs))

        turl1 = dot.prefix(target1)
        turl2 = dot.prefix(target2)
        result += "\n" + dot.arrow(point, turl1, attrs=labeldict(label))
        result += "\n" + dot.arrow(point, turl2, attrs=attrs)
        return result

    return arrow2(dot, source, target1 if target1 else target2, label, extra)


garrow2 = partial(arrow2, labeldict=glabeldict)
garrow3 = partial(arrow3, labeldict=glabeldict, attrs={"color": "darkgreen"})
