from datetime import datetime

from taskifier import const
from taskifier.models import Task

class TaskPayloadHelper:
    def __init__(self, payload):
        for k, v in payload.items():
            setattr(self, k, v)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def get_ready_datetime(self):
        if self[const.KEY_READY_TIME]:
            return datetime.strptime(self[const.KEY_READY_TIME], '%Y-%m-%dT%H:%M:%S.%fZ')
        return None
    
    def is_duplicate(self):
        if not self.is_valid():
            return False;
        
        q = Task.objects.filter(source=self[const.KEY_SOURCE])
        q.filter(dest=self[const.KEY_DEST])
        q.filter(ready_time=self.get_ready_datetime())
        return q.count() > 0
    
    def is_valid(self):
        if (self[const.KEY_SOURCE] is None) or (self[const.KEY_DEST] is None) \
           or (self[const.KEY_CONTENT] is None) or (self[const.KEY_READY_TIME] is None):
            return False
        
        return True
