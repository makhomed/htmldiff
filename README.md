htmldiff
========
Tool for diffing html files

- Original is from [Ian Bicking](https://github.com/ianb)
- Updates and improvements from [Richard Cyganiak](https://github.com/cygri)
- Refactored for use with setup tools by [Brant Watson](https://github.com/induane)
- Modified by [Gena Makhomed](https://github.com/makhomed)

License: MIT

Installation
============
To build a source package:

    $ python setup.py sdist

To install into your current environment:

    $ python setup.py install

Or via pip:

    $ pip install .

Pip may also be used to install a built package:

    $ pip install htmldiff-1.0.0.dev7.tar.gz


Usage
=====

To produce a diff of two html files:

    $ htmldiff file1.html file2.html > diff_file.html

With custom output file:

    $ htmldiff file1.html file2.html -o diff_file.html

All options:

 * -h print command line help and exit
 * -v print application version and exit
 * -o OUTPUT_FILE write to given output file instead of stdout

