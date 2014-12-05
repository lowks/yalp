# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.parsers
============
'''
from .. import BaseYalp

import logging
logger = logging.getLogger(__name__)


class BaseParser(BaseYalp):
    '''
    Base parser.
    '''

    def __init__(self, type_=None, **kwargs):  # pylint: disable=W0613
        self.type_ = type_

    def parse(self, event):
        '''
        Parse the log message.
        '''
        if self.type_ != event.get('type', None):
            logger.info('%s skipping event %s: not same type',
                        self.__class__.__name__,
                        event)
        else:
            from yalp.outputs import tasks
            tasks.process_output.delay(event)
            return event['message']
