from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

import json

from taskifier import const
from taskifier.models import Task, TaskOwner
from taskifier.internal.TaskPayloadHelper import TaskPayloadHelper

EMPTY_RESP = {}

def DELETE(task_owner, task_id):
    task = _get_task_by_id(task_id)
    if task and _is_owner(task_owner, task):
        task.delete()
        
        return {const.KEY_ID: task_id,
                const.KEY_SOURCE: "",
                const.KEY_DEST: "",
                const.KEY_CONTENT: "",
                const.KEY_READY_TIME: ""}
    return EMPTY_RESP

def GET(task_owner, task_id):
    task = _get_task_by_id(task_id)
    
    if task and _is_owner(task_owner, task):
        return {const.KEY_ID: task_id,
                const.KEY_SOURCE: task.source,
                const.KEY_DEST: task.dest,
                const.KEY_CONTENT: task.content,
                const.KEY_READY_TIME: _get_json_from_datetime(task.ready_time)}
    return EMPTY_RESP
    
def POST(task_owner, task_id, request_payload):
    taskPayloadHelper = TaskPayloadHelper(request_payload)
    if not taskPayloadHelper.is_valid() or taskPayloadHelper.is_duplicate():
        return EMPTY_RESP
    
    if task_id is None:
        task = Task(owner=task_owner,
                    source=taskPayloadHelper[const.KEY_SOURCE],
                    dest=taskPayloadHelper[const.KEY_DEST],
                    content=taskPayloadHelper[const.KEY_CONTENT],
                    ready_time=taskPayloadHelper.get_ready_datetime())
        task.save()
        task_id = task.id
    else:
        task = _get_task_by_id(task_id)
        task.source = taskPayloadHelper[const.KEY_SOURCE]
        task.dest = taskPayloadHelper[const.KEY_DEST]
        task.content = taskPayloadHelper[const.KEY_CONTENT]
        task.ready_time = taskPayloadHelper.get_ready_datetime()
        task.save()
    
    return {const.KEY_ID: task_id,
            const.KEY_SOURCE: taskPayloadHelper[const.KEY_SOURCE],
            const.KEY_DEST: taskPayloadHelper[const.KEY_DEST],
            const.KEY_CONTENT: taskPayloadHelper[const.KEY_CONTENT],
            const.KEY_READY_TIME: taskPayloadHelper[const.KEY_READY_TIME]}

def get_owner(owner_key):
    query_set = TaskOwner.objects.filter(key=owner_key)
    if query_set and (len(query_set) == 1):
        return query_set[0]
    else:
        return None

def _get_json_from_datetime(obj):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    json_str = json.dumps(obj, default=dthandler)
    json_str = json_str.replace('"', '')
    json_str = _rreplace(json_str, "000", "Z")
    return json_str

def _get_task_by_id(task_id):
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

def _rreplace(s, old, new):
    offset = 0 - len(old)
    remainder = s[:offset]
    replace_array = s.split(remainder)
    replace_confirm = replace_array[(len(replace_array) - 1)]
    if replace_confirm == old:
        return s[:-len(old)] + new
    return s
