from django.http import HttpRequest
from django.test import TestCase

import json

from taskifier import const
from taskifier import taskrouter
from taskifier.models import TaskOwner

class FullRunTestCase(TestCase):
    def setUp(self):
        self.taskowner = TaskOwner(email='example@example.com', key='example')
        self.taskowner.save()
    
    def test_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = {const.KEY_ID: "",
                        const.KEY_SOURCE: "a@domain.com",
                        const.KEY_DEST: "b@domain.com",
                        const.KEY_CONTENT: "text content",
                        const.KEY_READY_TIME: "2013-09-13T04:22:58.578Z"}
        response = taskrouter(request=request,
                              owner_key=self.taskowner.key,
                              task_id=None)
        
        response_body = response.content
        self.assertTrue(response_body)
        
        json_body = json.loads(response_body)
        self.assertTrue(json_body)
        
        self.assertEqual(json_body[const.KEY_SOURCE], request.POST[const.KEY_SOURCE])
        self.assertEqual(json_body[const.KEY_DEST], request.POST[const.KEY_DEST])
        self.assertEqual(json_body[const.KEY_CONTENT], request.POST[const.KEY_CONTENT])
        self.assertEqual(json_body[const.KEY_READY_TIME], request.POST[const.KEY_READY_TIME])
    
    def test_GET(self):
        return
    
    def test_DELETE(self):
        return