from raidgear.tests import *

class TestCharacterController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='character', action='index'))
        # Test response...
