import errno
import re
import os

GITHUB = "https://github.com/dew-uff/mutable-prov"
BASE = "."

def exists(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename
        )

def all_replaces(text):
    variables = {}

    def set_var(match):
        variables[match.group(1).strip()] = match.group(2).strip()
        return ""

    def get_var(match):
        return variables[match.group(1).strip()]

    def link(match):
        name = match.group(2)
        exists(os.path.join(BASE, name))
        return "[{}]({})".format(
            match.group(1),
            GITHUB + "/raw/master/" + name,
        )

    def image(match):
        name = match.group(2)
        exists(os.path.join(BASE, name + ".png"))
        exists(os.path.join(BASE, name + ".pdf"))
        return "[![{}]({})]({})".format(
            match.group(1).format(**variables),
            GITHUB + "/raw/master/" + name + ".png",
            GITHUB + "/blob/master/" + name + ".pdf",
        )

    def prov(match):
        name = match.group(2)
        exists(os.path.join(BASE, name + ".png"))
        exists(os.path.join(BASE, name + ".pdf"))
        result = []
        result.append("```provn")
        with open(os.path.join(BASE, name + ".provn"), "r") as f:
            provn = f.read()
            pos = provn.find("// new")
            if pos != -1:
                provn = provn[pos+6:]
            result.append(provn.strip())
        result.append("```")
        result.append("")
        result.append("[![{}]({})]({})".format(
            match.group(1),
            GITHUB + "/raw/master/" + name + ".png",
            GITHUB + "/blob/master/" + name + ".pdf",
        ))
        return "\n".join(result)

    def load(match):
        name = match.group(1)
        with open(os.path.join(BASE, name), "r") as f:
            return f.read().strip()

    text = re.sub(r"::SET\s+(.*?)\s*=\s*(.*?)::", set_var, text)
    text = re.sub(r"::GET\s+(.*?)\s*::", get_var, text)
    text = re.sub(r"::\[(.*?)\]\((.*?)\)", link, text)
    text = re.sub(r"::!\[(.*?)\]\((.*?)\)", image, text)
    text = re.sub(r"::PROV\[(.*?)\]\((.*?)\)", prov, text)
    text = re.sub(r"::LOAD\((.*?)\)", load, text)
    return text.strip()


if __name__ == "__main__":
    for root, dirs, files in os.walk(os.path.join(BASE, "source")):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), "r") as r, open(os.path.join(BASE, file), "w") as w:
                    w.write(all_replaces(r.read()))
