# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers.passthrough
========================
'''
from . import BaseParser


class Parser(BaseParser):
    '''
    Print input
    '''
    def __init__(self, *args, **kwargs):
        super(Parser, self).__init__(*args, **kwargs)

    def parse(self, event):
        return event
