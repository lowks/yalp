# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.inputs
===========
'''
from datetime import datetime

from ..config import settings
from ..utils import get_hostname
from ..pipeline import ThreadPipline

import logging

_DATE_FMT = '%Y-%m-%dT%H:%M:%S'


class BaseInputer(ThreadPipline):
    ''' Base Inputer '''

    def __init__(self, *args, **kwargs):
        super(BaseInputer, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.hostname = get_hostname()

    def enqueue_event(self, event):
        '''
        Take an event and send it to the proper queue.

        Send the event to the parsers queue, unless there are no parsers
        in the config. Then send the event directly to the outputs.
        '''
        if self.type_:
            event['type'] = self.type_
        event['hostname'] = self.hostname
        if 'time_stamp' not in event:
            event['time_stamp'] = datetime.now().strftime(_DATE_FMT)
        from yalp.pipeline import tasks
        if settings.parsers:
            tasks.process_message.apply_async(
                args=[event],
                queue=settings.parser_queue,
                serializer=settings.celery_serializer,
            )
        else:
            tasks.process_output(event)
