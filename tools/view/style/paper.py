from tools.view.style.specific import DotSpecific
from functools import partial
import re

class DotPaper(DotSpecific):

    def __init__(self, **kwargs):
        super(DotPaper, self).__init__(**kwargs)
        self.specific2 = "#800000"
        self.specific1 = "#ffe6e6"
        self.style = self.join(self.style, {
            "ver_wasDerivedFrom0": {"style":"dashed", "color": self.specific2},
            "ver_wasDerivedFrom2_label*": self.custom_label,
        })

    def custom_label(self, label, attrs):
        return self.join(self.label(label, attrs), {
            "fontcolor": self.specific2
        })


    def taillabel(self, label, attrs):
        if "dot:specific" in attrs:
            return self.label(label, attrs, color=self.specific1)
        return super().taillabel(label, attrs)

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
                "labelfontsize": "8",
                "labeldistance": "1.5",
                "color": color,
                "labelangle": "60.0",
                "rotation": "20",
                "label": label
            }
        return {"color": color}


EXPORT = DotPaper