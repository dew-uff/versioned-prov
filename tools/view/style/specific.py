from tools.view.style.hide import DotHide

class DotSpecific(DotHide):

    def __init__(self, specific1="darkgreen", specific2="green", **kwargs):
        super(DotSpecific, self).__init__(**kwargs)
        self.specific1 = specific1
        self.specific2 = specific2

    def dotchange(self, statement, args, current, attrs):
        result = super(DotSpecific, self).dotchange(statement, args, current, attrs)
        if "dot:specific" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = self.specific1
            result["fontcolor"] = self.specific2
            result["color"] = self.specific2
        return result

    def filter_attr(self, key, value, attrs):
        if "dot:hide" in attrs:
            return False
        return not key.startswith("dot:")

EXPORT = DotSpecific