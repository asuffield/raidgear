from raidgear.tests import *

class TestMenuController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='menu', action='index'))
        # Test response...
