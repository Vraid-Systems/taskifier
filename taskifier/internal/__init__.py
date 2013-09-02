from django.core.exceptions import ObjectDoesNotExist

from taskifier import const
from taskifier.models import Task, TaskOwner

EMPTY_RESP = {}

def DELETE(task_owner, task_id):
    task = get_task_by_id(task_id)
    if task and _is_owner(task_owner, task):
        task.delete()
        
        return {const.RESP_KEY_ID: task_id,
                const.RESP_KEY_SOURCE: "",
                const.RESP_KEY_DEST: "",
                const.RESP_KEY_CONTENT: ""}
    return EMPTY_RESP

def GET(task_owner, task_id):
    task = get_task_by_id(task_id)
    
    if task and _is_owner(task_owner, task):
        return {const.RESP_KEY_ID: task_id,
                const.RESP_KEY_SOURCE: task.source,
                const.RESP_KEY_DEST: task.dest,
                const.RESP_KEY_CONTENT: task.content}
    return EMPTY_RESP
    
def POST(task_owner, task_id, request_payload):
    if _is_valid_payload(request_payload) == False:
        return EMPTY_RESP
    
    if task_id is None:
        # --> TODO pull in ready_time <--
        task = Task(owner=task_owner, source=request_payload.source,
                    dest=request_payload.dest, content=request_payload.content)
        task.save()
        task_id = task.id
    else:
        task = get_task_by_id(task_id)
        task.source = request_payload.source
        task.dest = request_payload.dest
        task.content = request_payload.content
        task.save()
    
    return {const.RESP_KEY_ID: task_id,
            const.RESP_KEY_SOURCE: request_payload.source,
            const.RESP_KEY_DEST: request_payload.dest,
            const.RESP_KEY_CONTENT: request_payload.content}

def get_owner(owner_key):
    query_set = TaskOwner.objects.filter(key=owner_key)
    if query_set and (len(query_set) == 1):
        return query_set[0]
    else:
        return None

def get_task_by_id(task_id):
    if task_id:
        task = None
        try:
            task = Task.objects.get(id=task_id)
        except ObjectDoesNotExist:
            task = None
        return task
    else:
        return None

def _is_owner(task_owner, task):
    if task and task_owner and isinstance(task, Task) and isinstance(task_owner, TaskOwner):
        return (task_owner.key == task.owner.key)
    else:
        return False

def _is_valid_payload(request_payload):
    if len(request_payload) != 3:
        return False
    
    if (request_payload.source is None) or (request_payload.dest is None) or (request_payload.content is None):
        return False
    
    return True
