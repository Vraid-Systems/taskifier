import re

class WorkerHelper:
    def __init__(self):
        # re.compile discussion
        # http://stackoverflow.com/questions/452104/is-it-worth-using-pythons-re-compile
        # did not want to rely on framework assumptions
        self.RE_EMAIL = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        self.RE_TWITTER = re.compile(r'^\@([\w]{1,15})$')

    def isEmail(self, theEmail):
        # http://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
        # "There is no point."++
        if self.RE_EMAIL.match(theEmail):
            return True
        return False

    def isTwitterHandle(self, theHandle):
        if self.RE_TWITTER.match(theHandle):
            return True
        return False
