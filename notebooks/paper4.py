from extensible_provn.view.style.paper import DotPaper
import re


class DotPaper4(DotPaper):

    def __init__(self, **kwargs):
        super(DotPaper4, self).__init__(**kwargs)
        self.use_parsetime = True
        self.hide_namespace = True
        self.labelsize = "20"
        self.node_labelsize = "20"
        self.tail_labelsize = "16"
        self.attrs_labelsize = "13"
        self.specific2 = "#800000"
        self.specific1 = "#ffe6e6"
        
    def taillabel(self, label, attrs):
        if "dot:specific" in attrs:
            return self.label(label, attrs, color=self.specific1)
        if label:
            return {
                "labelfontsize": self.tail_labelsize,
                "labeldistance": attrs.get("dot:dist", "1"),
                "labelangle": attrs.get("dot:angle", "60.0"),
                "rotation": "20",
                "taillabel": label.replace('"', '\\"')
            }
        return {}

    def label(self, label, attrs, color="black"):
        if label:
            if color == "black" and not "dot:hide2" in attrs and not "dot:specific" in attrs:

                split = re.split(r'( |\n)', label)
                part1 = '<font color="{}">{}</font>'.format(color, split[0])
                part2 = ""
                if len(split) > 1:
                    part2 = "".join(split[1:]).replace("\n", "<br/>")
                    part2 = '<font color="{}">{}</font>'.format(self.specific2, part2)
                label = ("<{}{}>".format(part1, part2))
            else:
                label = label.replace('"', '\\"')
            return {
                "fontsize": self.labelsize,

                "labeldistance": attrs.get("dot:dist", "1"),
                "color": color,
                "labelangle": attrs.get("dot:angle", "60.0"),
                "rotation": "20",
                "label": label
            }
        return {"color": color}

        
EXPORT = DotPaper4