""" MD2Slide

NAME
	md2slide - markdown to slide

SYNOPSIS
	md2slide [OPTION] [Directory]

DESCRIPTION
    -h, --help
            show usage

    -v, --verbose

EXAMPLES
    md2slide /path/to/my/mdslide

COPYRIGHT
	MIT Licence

SOURCE
    https://github.com/yanganto/MD2Slide
"""

import sys
import getopt
import logging
from server import run


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hv", ["help", "verbose"])
    except getopt.GetoptError as e:
        print(__doc__)
        sys.exit("invalid option: " + str(e))

    for o, a in opts:
        if o in ('-h', '--help'):
            print(__doc__)
            sys.exit(0)
        elif o in ('-v', '--verbose'):
            logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
    if args:
        run(args[0])
    run()

if __name__ == "__main__":
    if sys.argv:
        main(sys.argv[1:])
    main()
