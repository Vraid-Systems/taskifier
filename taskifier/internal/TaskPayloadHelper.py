from taskifier.models import Task

class TaskPayloadHelper:
    def __init__(self, payload=None):
        self.payload = payload
    
    def get_datetime_obj(self):
        # !!! TODO add method functionality !!! #
        return self.payload.ready_time
    
    def is_duplicate(self):
        if self.payload is None:
            return False;
        
        q = Task.objects.filter(source=self.payload.source)
        q.filter(dest=self.payload.dest)
        q.filter(ready_time=self.payload.ready_time)
        return q.count() > 0
    
    def is_valid(self):
        if self.payload is None:
            return False
        
        if len(self.payload) != 4:
            return False
        
        if (self.payload.source is None) or (self.payload.dest is None) \
           or (self.payload.content is None) or (self.payload.ready_time is None):
            return False
        
        return True
