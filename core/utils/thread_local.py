import threading
from core.abstractions import SingletonClass
from uuid import uuid4


_EVENT_ID = 'event_id'
_EXCEPTION = 'exception'


class EventLogging(SingletonClass):
    """[summary]
    """

    def _singleton_init(self, **kwargs):
        """[summary]
        """
        self._local_eid = threading.local()
        self._local_exc = threading.local()

    def handle_new_request(self):
        self.set_event_id()
        self.clear_current_exc()

    def set_event_id(self, event_id=''):
        if not event_id or not isinstance(event_id, str):
            event_id = str(uuid4())

        setattr(self._local_eid, _EVENT_ID, event_id)

    def get_event_id(self) -> str:
        if not hasattr(self._local_eid, _EVENT_ID) or not getattr(self._local_eid, _EVENT_ID):
            self.set_event_id()
        return getattr(self._local_eid, _EVENT_ID)

    def set_current_exc(self, exc):
        if not exc or not isinstance(exc, Exception):
            return
        setattr(self._local_exc, _EXCEPTION, exc)

    def clear_current_exc(self):
        setattr(self._local_exc, _EXCEPTION, None)

    def get_current_exc(self) -> Exception:
        return getattr(self._local_exc, _EXCEPTION, None)

    def clear_event_id(self):
        setattr(self._local_eid, _EVENT_ID, None)

    def clear_all(self):
        self.clear_event_id()
        self.clear_current_exc()


elog: EventLogging = EventLogging()
