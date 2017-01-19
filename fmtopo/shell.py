"""Flow Manager Testing Tools

Usage:
  fmcheck links [-s] [--topology=FILE] [--controller=IP]...
  fmcheck nodes [-s] [--topology=FILE] [--controller=IP]...
  fmcheck flows [-a] [--topology=FILE] [--controller=IP]...
  fmcheck (-h | --help)

Options:
  -h --help     Show this screen.
  -t, --topology=FILE   Topolofy file name [default: fm-topo.yml].
  -c, --controller=IP   Controller IP address
  -s --stopped      If Mininet is not running.
  -a --check-stats  Check flow/groups states with previous check
  --version     Show version.

"""

import os
import sys
import yaml
from docopt.docopt import docopt
import fmtopo.topo


class Shell(object):

    def __init__(self):
        arguments = docopt(__doc__, version='Flow Manager Testing Tools 1.0')

        file = 'fm-topo.yml'
        if arguments['--topology']:
            file = arguments['--topology']

        props = None
        if (os.path.isfile(file)):
            with open(file, 'r') as f:
                props = yaml.load(f)

        if props is None:
            print "ERROR: yml topology file not found"
            sys.exit()

        if arguments['--controller']:
            props['controller'] = []
            i = 0
            for ip in arguments['--controller']:
                props['controller'].append(
                    {'name': "c{}".format(i),
                     'ip': ip
                     })
                i = i + 1

        checker = fmtopo.topo.Topo(props)
        if arguments['links'] and arguments['--stopped']:
            result = checker.check_links(False)
        elif arguments['links']:
            result = checker.check_links()
        elif arguments['flows'] and arguments['--check-stats']:
            result = checker.check_flows(check_stats=True)
        elif arguments['flows']:
            result = checker.check_flows()
        elif arguments['nodes'] and arguments['--stopped']:
            result = checker.check_nodes(False)
        elif arguments['nodes']:
            result = checker.check_nodes()

        if not result:
            sys.exit(1)

def main():
    Shell()

if __name__ == "__main__":
    Shell()