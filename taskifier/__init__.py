import const, json
from django.http import HttpResponse, HttpResponseRedirect
from taskifier.api import DELETE, GET, POST, get_owner
from taskifier.models import TaskOwner

CONTENT_TYPE_JSON = "application/json"

def taskrouter(request, owner_key = None, task_id = None):
    """route data request to correct handler and return JSON HttpResponse
    
    Args:
        request: the HttpRequest object
        owner_key: string finger print of the user
        task_id: a numeric identifier for the task
    
    Returns:
        HttpResponse - JSON
    """
    EMPTY_RESP = {}
    
    task_owner = None
    if owner_key:
        task_owner = get_owner(owner_key)
    
    if request.method == 'OPTIONS':
        return getJsonHttpResponse(EMPTY_RESP)
    
    if request.method == 'POST':
        if request.POST:
            return getJsonHttpResponse(POST(task_owner=task_owner,
                                            task_id=task_id,
                                            request_payload=request.POST))
    
    if request.method == 'GET':
        return getJsonHttpResponse(GET(task_owner, task_id))
    
    if request.method == 'DELETE':
        return getJsonHttpResponse(DELETE(task_owner, task_id))
    
    return getJsonHttpResponse(EMPTY_RESP)

def addCORSHeaders(theHttpResponse):
    if theHttpResponse and isinstance(theHttpResponse, HttpResponse):
        theHttpResponse['Access-Control-Allow-Origin'] = '*'
        theHttpResponse['Access-Control-Max-Age'] = '120'
        theHttpResponse['Access-Control-Allow-Credentials'] = 'true'
        theHttpResponse['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
        theHttpResponse['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
    return theHttpResponse

def getJsonHttpResponse(response):
    aHttpResponse = HttpResponse(json.dumps(response), content_type=CONTENT_TYPE_JSON)
    return addCORSHeaders(aHttpResponse)
