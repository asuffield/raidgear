import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from raidgear.lib.base import BaseController, render

from raidgear.model.meta import Session
from raidgear.model import Character

log = logging.getLogger(__name__)

class MenuController(BaseController):

    def index(self):
        c.chars = Session.query(Character).all()
        
        return render('index.html')

    def character(self):
        character = request.params.get('charname', '')
        if character == '':
            character = request.params.get('character', '')
        if character == '':
            redirect(url(controller='menu', action='index'))

        redirect(url(controller='character', action='view', charname=character))
