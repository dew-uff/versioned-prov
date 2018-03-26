import errno
import re
import os
import pypandoc

GITHUB = "https://github.com/dew-uff/versioned-prov"
GITHUBIO = "https://dew-uff.github.io/versioned-prov"
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
    text = text.replace("\r\n", "\n")
    return text.strip()


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Versioned-PROV</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <link href="css/github.css" rel="stylesheet">
    <link href="css/style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <a class="navbar-brand" href="#">Versioned-PROV</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
            {}
        </ul>
        <ul class="navbar-nav navbar-right ">
            <li class="nav-item"><a class="nav-link" href="https://github.com/dew-uff/versioned-prov"><span class="hidden-xs-down"> View on GitHub </span><svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-mark-github" aria-hidden="true"><path id="githublogo" fill="rgb(157, 157, 157)" fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg></a></li>
          </ul>
      </div>
    </nav>
    <div class="container">
      <div class="starter-template">
        {}
      </div>
    </div>
    <footer class="footer">
      <img height="50" alt="Universidade Federal Fluminense - Instituto da Computa&ccedil;&atilde;o"  title="Universidade Federal Fluminense - Instituto da Computa&ccedil;&atilde;o" src="images/ic.jpg">
      <img height="50" alt="Newcastle University - School of Computing" title="Newcastle University - School of Computing" src="images/newcastle.svg">
    </footer>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
"""
HEADER = {
    "README.md": '<span class="navbar-align">Home{}</span>',
    "prov.md": 'PROV<span class="mapping">Mapping</span>{}',
    "prov-dictionary.md": 'PROV-Dictionary<span class="mapping">Mapping</span>{}',
    "versioned-prov.md": 'Versioned-PROV<span class="mapping">Mapping</span>{}',
    "comparison.md": '<span class="navbar-align">Comparison{}</span>',
}



if __name__ == "__main__":
    for root, dirs, files in os.walk(os.path.join(BASE, "source")):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), "r") as r:
                    result = all_replaces(r.read())
                    #with open(os.path.join(BASE, file), "w") as w:
                    #    w.write(result)
                    with open(os.path.join("docs", file.replace(".md", ".html")), "w") as w:
                        header = []
                        for key, value in HEADER.items():
                            active = ""
                            current = ""
                            if key == file:
                                active = " active"
                                current = '<span class="sr-only">(current)</span>'
                            href = key.replace(".md", ".html")
                            header.append('<li class="nav-item">')
                            header.append('<a class="nav-link{}" href="{}">'.format(active, href))
                            header.append(value.format(current))
                            header.append("</a>")
                            header.append('</li>')

                        html = TEMPLATE.format("".join(header), pypandoc.convert_text(result, 'html', format='markdown_github')).replace("\r\n", "\n")
                        html = html.replace("width:44%", "width:100%")
                        w.write(html)