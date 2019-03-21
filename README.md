htmldiff
========
HTML Diffing utility.

- Original is from [Ian Bicking](https://github.com/ianb)
- Updates and improvements from [Richard Cyganiak](https://github.com/cygri)
- Refactored for use with setup tools by [Brant Watson](https://github.com/induane)
- Modified by [Gena Makhomed](https://github.com/makhomed)

License: MIT

Installation
============
To build a source package::

    $ python setup.py sdist

To install into your current environment::

    $ python setup.py install

Or via pip::

    $ pip install .

Pip may also be used to install a built package::

    $ pip install htmldiff-1.0.0.dev7.tar.gz


Usage
=====

To produce a diff of two html files::

    $ htmldiff file1.html file2.html > diff_file.html

With custom output file::

    $ htmldiff file1.html file2.html -o diff_file.html

All options:

 * -o --output-file OUTPUT_FILE [Optional] Specify a custom output file
 * -l --log-level (DEBUG,INFO,WARNING,ERROR,CRITICAL)
 * -L --log-file Location to place logging output
 * -v --version Print the application version and exit
 * -h --help Print command line help
