"""
Entry Point
-----------
Command-line entry point
"""
# Standard
import argparse
import os
import os.path
import pkg_resources
import sys
import time

# Project
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
    except Exception as e:
        eprint(e, '\nDiff process exited with an error\n')
        sys.exit(1)

    if output_file is None:
        sys.stdout.write(diffed_html)
    else:
        try:
            with open(output_file, 'w') as f:
                f.seek(0)
                f.truncate()
                f.write(diffed_html)
        except Exception as e:
            eprint(e, '\nUnable to write diff to {0}\n'.format(output_file))
            sys.exit(1)

def main():
    start_time = time.time()
    try:
        diff()
    except KeyboardInterrupt:
        eprint("\nOperation canceled by user\n")
        sys.exit(1)
    eprint('Took {0:0.4f} seconds\n'.format(time.time() - start_time))

if __name__ == '__main__':
    main()
