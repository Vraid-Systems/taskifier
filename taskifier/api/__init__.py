from taskifier.internal import DELETE as int_DELETE
from taskifier.internal import GET as int_GET
from taskifier.internal import POST as int_POST
from taskifier.internal import get_owner as int_get_owner

def DELETE(task_owner, task_id):
    """Delete a queued task
    
    Args:
        task_owner: the owner Model
        task_id: a numeric identifier for task
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {const.KEY_ID: task_id,
         const.KEY_SOURCE: "",
         const.KEY_DEST: "",
         const.KEY_CONTENT: "",
         const.KEY_READY_TIME: ""}
    """
    return int_DELETE(task_owner, task_id)

def GET(task_owner, task_id):
    """Get a queued task
    
    Args:
        task_owner: the owner Model
        task_id: a numeric identifier for task
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {const.KEY_ID: task_id,
         const.KEY_SOURCE: task.source,
         const.KEY_DEST: task.dest,
         const.KEY_CONTENT: task.content,
         const.KEY_READY_TIME: task.ready_time}
    """
    return int_GET(task_owner, task_id)

def POST(task_owner, task_id, request_payload):
    """Add/update a task to/in the queue
    
    Args:
        task_owner: the owner Model
        task_id: a numeric identifier for task (only if updating existing object)
        request_payload: an instance of django.http.QueryDict with source, dest, content, ready time fields
    
    Returns:
        A dictionary for creating a HTTP response. Example:
        {const._KEY_ID: task_id,
         const.KEY_SOURCE: request_payload.source,
         const.KEY_DEST: request_payload.dest,
         const.KEY_CONTENT: request_payload.content,
         const.KEY_READY_TIME: request_payload.ready_time}
    """
    return int_POST(task_owner, task_id, request_payload)

def get_owner(owner_key):
    """Retrieve the TaskOwner object via the owner_key
    
    Args:
        owner_key: string finger print of the user
    
    Returns:
        TaskOwner
    """
    return int_get_owner(owner_key)
