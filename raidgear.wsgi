import os, sys 
__here__ = os.path.dirname(__file__) 
sys.path.append(__here__) 
from paste.script.util.logging_config import fileConfig 
fileConfig('%s/production.ini' % __here__) 
from paste.deploy import loadapp 
application = loadapp('config:%s/production.ini' % __here__) 
