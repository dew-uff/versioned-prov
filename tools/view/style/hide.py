from tools.view.style.dot import DotNoHighlight

class DotHide(DotNoHighlight):

    def __init__(self, hide1="#FAFAFA", hide2="#F0F0F0", **kwargs):
        super(DotHide, self).__init__(**kwargs)
        self.hide1 = hide1
        self.hide2 = hide2

    def dotchange(self, statement, args, current, attrs):
        result = super(DotHide, self).dotchange(statement, args, current, attrs)

        if "dot:hide" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = self.hide1
            result["fontcolor"] = self.hide2
            result["color"] = self.hide2
        if "dot:specific" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = "darkgreen"
            result["fontcolor"] = "green"
            result["color"] = "green"
        return result

    def filter_attr(self, key, value, attrs):
        if "dot:hide" in attrs:
            return False
        return not key.startswith("dot:")

EXPORT = DotHide