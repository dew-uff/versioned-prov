import subprocess
import platform
import errno

from IPython.display import display, Image, SVG
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from dot import graph

STARTUPINFO = None

if platform.system().lower() == 'windows':
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    STARTUPINFO.wShowWindow = subprocess.SW_HIDE


@magics_class
class ProvMagic(Magics):
    @magic_arguments()
    @argument('-d', '--dot', default=None, type=str, help="Output dot file")
    @argument('-e', '--engine', default="dot", type=str, help="Command for rendering (dot, neato, ...)")
    @argument('-o', '--output', default="temp.svg", type=str, help="Output image file")
    @argument('-x', '--width', default=16, type=int, help="Graph width")
    @argument('-y', '--height', default=12, type=int, help="Graph height")
    @argument('-r', '--rankdir', default="BT", type=str, help="Graph rankdir")
    @cell_magic
    def provn(self, line, cell):
        graph.reset_config()
        # Remove comment on %%provn line
        pos = line.find("#")
        line = line[:pos if pos != -1 else None]
        args = parse_argstring(self.provn, line)

        graph.size_x = args.width
        graph.size_y = args.height
        graph.rankdir = args.rankdir
        # Dot header
        pos = cell.find("##H##")
        if pos != -1:
            graph.header = cell[:pos]
            cell = cell[pos+5:]

        # Dot footer
        pos = cell.find("##F##")
        if pos != -1:
            graph.footer = cell[pos + 5:]
            cell = cell[:pos]

        dot_content = graph.generate(cell)

        split = args.output.split(".")
        if len(split) > 1:
            dext = ext = split[-1]
            name = split[:-1]
        else:
            dext = ext = "svg"
            name = [args.output]
        if ext.lower() != "png":
            dext = "svg"

        dot_file = args.dot
        if dot_file is None:
            dot_file = ".".join(name + ["dot"])

        with open(dot_file, "w") as f:
            f.write(dot_content)

        dimage = ".".join(name + [dext])

        draw_args = [args.engine, dot_file, "-T{}".format(dext), "-o", dimage]
        subprocess.check_call(draw_args, startupinfo=STARTUPINFO)

        if ext.lower() == "pdf":
            try:
                ink_args = ["inkscape", "-D", "-z", "--file={}".format(dimage),
                            "--export-pdf={}".format(args.output)]
                subprocess.check_call(ink_args, startupinfo=STARTUPINFO)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    dot_args = [args.engine, "-Tpdf", "-o", args.output, dot_file]
                    subprocess.check_call(dot_args, startupinfo=STARTUPINFO)

        if dext.lower() == "svg":
            return SVG(filename=dimage)
        return Image(dimage)

def load_ipython_extension(ipython):
    ipython.register_magics(ProvMagic)
