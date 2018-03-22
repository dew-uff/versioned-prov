from tools.view.style.specific import DotSpecific

class DotPaper(DotSpecific):

    def __init__(self, **kwargs):
        super(DotPaper, self).__init__(**kwargs)
        self.style = self.join(self.style, {
            "ver_wasDerivedFrom0": {"style":"dashed", "color": self.specific2},
        })


    def taillabel(self, label, attrs):
        if "dot:specific" in attrs:
            return self.label(label, attrs, color=self.specific1)
        return super().taillabel(label, attrs)

    def label(self, label, attrs, color="black"):
        if label:
            return {
                "labelfontsize": "8",
                "labeldistance": "1.5",
                "color": color,
                "labelangle": "60.0",
                "rotation": "20",
                "label": label.replace('"', '\\"')
            }
        return {"color": color}


EXPORT = DotPaper