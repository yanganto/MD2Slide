""" MD2Slide

NAME
	md2slide - markdown to slide

SYNOPSIS
	md2slide [OPTION] [Directory]

DESCRIPTION
    -h, --help
            show usage

    -p, -port
            assign the port number of web server

    -v, --verbose

EXAMPLES
    # see the tutorial
    md2slide

    # see the mdslide in the folder
    md2slide /path/to/my/mdslide
    md2slide -p 8000 /path/to/my/mdslide

COPYRIGHT
	MIT Licence

SOURCE
    https://github.com/yanganto/MD2Slide
"""

import sys
import getopt
import logging
import os
import inspect
from md2slide.server import run


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hp:v", ["help", "port", "verbose"])
    except getopt.GetoptError as e:
        print(__doc__)
        sys.exit("invalid option: " + str(e))

    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    port = 8000
    if args:
        path = args[0]

    for o, a in opts:
        if o in ('-h', '--help'):
            print(__doc__)
            sys.exit(0)
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-v', '--verbose'):
            logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
    run(path, port=port)

if __name__ == "__main__":
    if sys.argv:
        main(sys.argv[1:])
    main()
