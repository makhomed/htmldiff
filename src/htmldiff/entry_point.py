"""
Entry Point
-----------
Command-line entry point
"""
import argparse
import codecs
import datetime
import os
import os.path
import pkg_resources
import sys
import traceback
from htmldiff.lib import diff_files, eprint

# Setup the version string
try:
    pkg_version = '%(prog)s {0}'.format(
        pkg_resources.get_distribution('htmldiff').version
    )
except pkg_resources.DistributionNotFound:
    pkg_version = '%(prog)s Development'
except Exception:
    pkg_version = '%(prog)s Unknown'


def diff():
    parser = argparse.ArgumentParser(
        description='Tool for diffing html files',
    )
    parser.add_argument('INPUT_FILE1')
    parser.add_argument('INPUT_FILE2')
    parser.add_argument(
        '-v',
        '--version',
        dest='version',
        action='version',
        version=pkg_version,
        help='show application version and exit'
    )
    parser.add_argument(
        '-o',
        action='store',
        dest='OUTPUT_FILE',
        default=None,
        help='write to given output file instead of stdout'
    )
    parsed_args = parser.parse_args()

    input_file1 = os.path.abspath(parsed_args.INPUT_FILE1)
    input_file2 = os.path.abspath(parsed_args.INPUT_FILE2)
    output_file = os.path.abspath(parsed_args.OUTPUT_FILE) if parsed_args.OUTPUT_FILE else None

    if not os.path.exists(input_file1):
        eprint('Could not find: {0}'.format(input_file1))
        sys.exit(1)

    if not os.path.exists(input_file2):
        eprint('Could not find: {0}'.format(input_file2))
        sys.exit(1)

    eprint('Diffing files...')
    try:
        diffed_html = diff_files(input_file1, input_file2)
    except Exception:
        traceback.print_exc()
        eprint('\nDiff process exited with an error\n')
        sys.exit(1)

    if output_file is None:
        sys.stdout.write(diffed_html.encode('UTF-8'))
    else:
        try:
            with codecs.open(output_file, 'w', encoding='UTF-8') as f:
                f.write(diffed_html)
        except Exception:
            traceback.print_exc()
            eprint('\nUnable to write diff to {0}\n'.format(output_file))
            sys.exit(1)

def main():
    start = datetime.datetime.now()
    try:
        diff()
    except KeyboardInterrupt:
        eprint("\nOperation canceled by user\n")
        sys.exit(1)
    end = datetime.datetime.now()
    eprint('Elapsed time '+str(end - start).split('.')[0]+'\n')

if __name__ == '__main__':
    main()
