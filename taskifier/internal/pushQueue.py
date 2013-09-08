from datetime import datetime
from google.appengine.api.app_identity import get_application_id
from google.appengine.api.mail import send_mail
from google.appengine.api.taskqueue import Task as queue_Task
from taskifier import const, getJsonHttpResponse
from taskifier.models import Task as db_Task
from taskifier.internal.WorkerHelper import WorkerHelper

def _create_task_from_db(db_Task_obj):
    if db_Task_obj is None:
        return None
    
    queue_Task_obj = queue_Task(payload=None, name=None,
                                method='POST', url='/pushqueue/worker',
                                headers={},
                                params={'source': db_Task_obj.source,
                                        'dest': db_Task_obj.dest,
                                        'content': db_Task_obj.content},
                                countdown=0)
    return queue_Task_obj

def cron(request): #called by cron.yaml through django
    db_Task_objs = _get_ready_tasks()
    if db_Task_objs is None:
        return getJsonHttpResponse({const.RESP_STATUS_KEY: "OK",
                                    const.RESP_STATUS_TEXT_KEY: "no stored tasks ready"})
    
    for db_Task_obj in db_Task_objs:
        queue_Task_obj = _create_task_from_db(db_Task_obj)
        if queue_Task_obj:
            queue_Task_obj.add(queue_name='send', transactional=False)
    
    _delete_processed_tasks(db_Task_objs)
    
    return getJsonHttpResponse({const.RESP_STATUS_KEY: "OK",
                                const.RESP_STATUS_TEXT_KEY: "stored tasks queued"})

def _get_ready_tasks():
    #lte filter --> http://stackoverflow.com/a/4668703
    #gt exclude --> https://docs.djangoproject.com/en/dev/ref/models/querysets/#exclude
    return db_Task.objects.filter(ready_time__lte=datetime.now())

def _delete_processed_tasks(db_Task_objs):
    for db_Task_obj in db_Task_objs:
        db_Task_obj.delete()

def worker(request): #called by queued task
    if request.POST and len(request.POST) == 3:
        workerHelper = WorkerHelper()
        if workerHelper.isEmail(request.POST.dest):
            send_mail(sender="app@"+get_application_id()+".appspotmail.com",
                      to=request.POST.dest,
                      subject="notification from "+request.POST.source,
                      body=request.POST.content,
                      reply_to=request.POST.source)
            
            return getJsonHttpResponse({const.RESP_STATUS_KEY: "OK",
                                        const.RESP_STATUS_TEXT_KEY: "email sent to "+request.POST.dest})
    
    return getJsonHttpResponse({const.RESP_STATUS_KEY: "FAIL",
                                const.RESP_STATUS_TEXT_KEY: "nothing to do"})
