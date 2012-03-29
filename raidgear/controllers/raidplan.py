import logging
from operator import itemgetter

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from raidgear.lib.base import BaseController, render

from raidgear.model.meta import Session
from raidgear.model import Character, Group, Faction, Instance, Mode

log = logging.getLogger(__name__)

class RaidplanController(BaseController):

    def view(self, faction):
        c.faction = Session.query(Faction).filter_by(name=faction).one()
        c.free_characters = Session.query(Character).filter_by(faction=c.faction, group=None).all()
        c.groups = Session.query(Group).filter_by(faction=c.faction).all()
        c.instances = Session.query(Instance).order_by(Instance.id.desc()).all()
        c.modes = Session.query(Mode).all()

        return render('plan.html')
