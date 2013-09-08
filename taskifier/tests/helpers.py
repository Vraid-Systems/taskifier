from django.test import TestCase

from taskifier.internal.WorkerHelper import WorkerHelper

TEST_EMAIL_CASES = ["user@domain.com", "@user@domain.com", "@cool_dude_ty", "user@domain.sub.com", "user@domain.com@.com"]
TEST_EMAIL_EXPECTS = [True, False, False, True, False]

TEST_TWITTER_CASES = ["user@domain.com", "@cool_dude_ty", "@cool-dude-ty", "@monkey.freud", "@___"]
TEST_TWITTER_EXPECTS = [False, True, False, False, True]

class WorkerHelperTestCase(TestCase):
    def setUp(self):
        self.workerHelper = WorkerHelper()
    
    def _array_test_helper(self, function, cases, expects):
        i = 0
        for case in cases:
            self.assertEqual(function(case), expects[i])
            i += 1
    
    def test_email_simple_validate(self):
        """a most basic email format check"""
        self._array_test_helper(self.workerHelper.isEmail, TEST_EMAIL_CASES, TEST_EMAIL_EXPECTS)

    def test_twitter_handle(self):
        """various Twitter handles are correctly identified"""
        self._array_test_helper(self.workerHelper.isTwitterHandle, TEST_TWITTER_CASES, TEST_TWITTER_EXPECTS)