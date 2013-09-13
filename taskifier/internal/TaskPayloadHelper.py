from datetime import datetime

from taskifier.models import Task

class TaskPayloadHelper:
    def __init__(self, payload):
        for k, v in payload.items():
            setattr(self, k, v)
    
    def get_ready_datetime(self):
        if self.ready_time:
            return datetime.strptime(self.ready_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        return None
    
    def is_duplicate(self):
        if not self.is_valid():
            return False;
        
        q = Task.objects.filter(source=self.source)
        q.filter(dest=self.dest)
        q.filter(ready_time=self.get_ready_datetime())
        return q.count() > 0
    
    def is_valid(self):
        if (self.source is None) or (self.dest is None) \
           or (self.content is None) or (self.ready_time is None):
            return False
        
        return True
