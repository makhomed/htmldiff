# vim: set fileencoding=utf-8 :
"""
.. module:: htmldiff.htmldiff
:synopsis: Utility to do inline diffs of html files.
.. moduleauthor:: Ian Bicking, Richard Cyganiak, Brant Watson
"""

from __future__ import print_function
from difflib import SequenceMatcher
from copy import copy

import codecs
import re
import StringIO
import sys


COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
TAG_RE = re.compile(r'<script.*?>.*?</script>|<.*?>', re.S)
HEAD_RE = re.compile(r'<\s*head\s*>', re.S | re.I)
WS_RE = re.compile(r'^([ \n\r\t]|&nbsp;)+$')
WORD_RE = re.compile(
    ur'''([^ \n\r\t,.&;:!?"«»“”/#=<>()-]+|(?:[ \n\r\t]|&nbsp;)+|[,.&;:!?"«»“”/#=<>()-])'''
)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TagIter(object):
    """Iterable that returns tags in sequence."""

    def __init__(self, html_string):
        self.html_string = html_string
        self.pos = 0
        self.end_reached = False
        self.buffer = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer:
            return self.buffer.pop(0)

        if self.end_reached:
            raise StopIteration

        match = TAG_RE.search(self.html_string, pos=self.pos)
        if not match:
            self.end_reached = True
            return self.html_string[self.pos:]

        self.buffer.append(match.group(0))
        val = self.html_string[self.pos:match.start()]
        self.pos = match.end()
        return val

    def next(self):
        return self.__next__()


class HTMLMatcher(SequenceMatcher):
    """SequenceMatcher for HTML data."""

    start_insert_text = '<span class="htmldiff-insert">'
    start_delete_text = '<span class="htmldiff-delete">'
    end_span_text = '</span>'
    stylesheet = (
            '.htmldiff-insert { background-color: #AFA; }\n'
            '.htmldiff-delete { background-color: #F88; }\n'
    )

    def __init__(self, source1, source2):
        SequenceMatcher.__init__(self, lambda x: False, source1, source2, False)

    def set_seqs(self, a, b):
        SequenceMatcher.set_seqs(self, self.split_html(a), self.split_html(b))

    def split_html(self, t):
        result = []
        for item in TagIter(t):
            if item.startswith('<'):
                result.append(item)
            else:
                result.extend(WORD_RE.findall(item))
        return result

    def diff_html(self, insert_stylesheet=True):
        opcodes = self.get_opcodes()
        a = self.a
        b = self.b
        out = StringIO.StringIO()
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                for item in a[i1:i2]:
                    out.write(item)
            if tag == 'delete':
                self.text_delete(a[i1:i2], out)
            if tag == 'insert':
                self.text_insert(b[j1:j2], out)
            if tag == 'replace':
                if (self.is_invisible_change(a[i1:i2], b[j1:j2])):
                    for item in b[j1:j2]:
                        out.write(item)
                else:
                    self.text_delete(a[i1:i2], out)
                    self.text_insert(b[j1:j2], out)
        html = out.getvalue()
        out.close()
        if insert_stylesheet:
            html = self.insert_stylesheet(html)
        return html

    def is_invisible_change(self, seq1, seq2):
        if len(seq1) != len(seq2):
            return False
        for i in range(0, len(seq1)):
            if seq1[i][0] == '<' and seq2[i][0] == '<':
                continue
            if all((WS_RE.match(seq1[i]), WS_RE.match(seq2[i]))):
                continue
            if seq1[i] != seq2[i]:
                return False
        return True

    def text_delete(self, lst, out):
        text = []
        for item in lst:
            if item.startswith('<'):
                self.out_delete(u''.join(text), out)
                text = []
            else:
                text.append(item)
        self.out_delete(u''.join(text), out)

    def text_insert(self, lst, out):
        text = []
        for item in lst:
            if item.startswith('<'):
                self.out_insert(u''.join(text), out)
                text = []
                out.write(item)
            else:
                text.append(item)
        self.out_insert(u''.join(text), out)

    def out_delete(self, s, out):
        if not s.strip():
            val = s
        else:
            val = u''.join((self.start_delete_text, s, self.end_span_text))
        out.write(val)

    def out_insert(self, s, out):
        if not s.strip():
            val = s
        else:
            val = u''.join((self.start_insert_text, s, self.end_span_text))
        out.write(val)

    def insert_stylesheet(self, html, stylesheet=None):
        """
        Add the stylesheet to the given html strings header. Attempt to find
        the head tag and insert it after it, but if it doesn't exist then
        insert at the beginning of the string.

        :type html: str
        :param html: string of html text to add the stylesheet to
        :type stylesheet: str
        :param stylesheet: css stylesheet to include in document header
        :returns: modified html string with stylesheet added to the header
        """
        if not stylesheet:
            stylesheet = self.stylesheet
        match = HEAD_RE.search(html)
        pos = match.end() if match else 0
        return ''.join((
            html[:pos],
            '\n<style type="text/css">\n',
            stylesheet,
            '</style>',
            html[pos:],
        ))


def diff_strings(orig, new):
    """
    Given two strings of html, return a diffed string.

    :type orig: string
    :param orig: original string for comparison
    :type new: string
    :param new: new string for comparision against original string
    :returns: string containing diffed html
    """
    h = HTMLMatcher(orig, new)
    return h.diff_html(True)


def diff_files(initial_path, new_path):
    """
    Given two files, open them to variables and pass them to diff_strings
    for diffing.

    :type initial_path: object
    :param initial_path: initial file to diff against
    :type new_path: object
    :param new_path: new file to compare to f1
    :returns: string containing diffed html from initial_path and new_path
    """
    # Open the files
    with codecs.open(initial_path, encoding='UTF-8') as f:
        source1 = COMMENT_RE.sub(u'', f.read())

    with codecs.open(new_path, encoding='UTF-8') as f:
        source2 = COMMENT_RE.sub(u'', f.read())

    return diff_strings(source1, source2)

