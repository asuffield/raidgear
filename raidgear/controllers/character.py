import logging
import re
from operator import itemgetter

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from raidgear.lib.base import BaseController, render

from raidgear.model.meta import Session
from raidgear.model import Character, Gear, Equipped, Instance, Spec, Faction, AdvClass

log = logging.getLogger(__name__)

class CharacterController(BaseController):

    def view(self, charname=None):
        if charname is None:
            redirect(url(controller='menu', action='index'))

        if not re.match(r'^[A-Za-z0-9_\'-]+$', charname):
            log.warn("Ignoring odd-looking character name '%s'" % charname)
            redirect(url(controller='menu', action='index'))

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            c.character = Character(charname)
            Session.add(c.character)
            Session.commit()

        c.equipped = {}
        c.form = {'faction': c.character.faction.name,
                  'spec': c.character.spec.name,
                  'advclass': c.character.advclass.name,
                  'ready': c.character.ready or None,
                  }
        for e in c.character.equipped:
            c.equipped[e.position()] = e
            c.form['equip_%d' % e.position()] = str(e.gear_id)

        log.debug(c.form)

        c.gear = Session.query(Gear).order_by(Gear.rank).order_by(Gear.pvp.desc()).all()
        c.spec = Session.query(Spec).order_by(Spec.id).all()
        c.factions = Session.query(Faction).order_by(Faction.id).all()
        c.advclasses = Session.query(AdvClass).order_by(AdvClass.name).all()

        self._advise()

        return render('char.html')

    def equip(self, charname=None):
        if charname is None:
            return

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            return

        position = int(request.params.get('slot', None))
        gear_id = int(request.params.get('gear', None))

        gear = Session.query(Gear).filter(Gear.id == gear_id).one()

        for e in c.character.equipped:
            if e.position() == position:
                e.gear = gear
                Session.commit()
                break

        self._advise()

        return render('advice.html')

    def faction(self, charname=None):
        if charname is None:
            return

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            return

        c.character.faction = Session.query(Faction).filter_by(name=request.params['value']).one()
        Session.commit()
        
        self._advise()

        return render('advice.html')

    def ready(self, charname=None):
        if charname is None:
            return

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            return

        c.character.ready = bool(request.params['value'])
        Session.commit()

    def spec(self, charname=None):
        if charname is None:
            return

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            return

        c.character.spec = Session.query(Spec).filter_by(name=request.params['value']).one()
        Session.commit()

    def advclass(self, charname=None):
        if charname is None:
            return

        c.character = Session.query(Character).filter(Character.name == charname).first()
        if c.character is None:
            return

        c.character.advclass = Session.query(AdvClass).filter_by(name=request.params['value']).one()
        Session.commit()

    def _score(self):
        c.score = c.character.gearscore()
        
    def _advise(self):
        bosses = {}
        c.faction = c.character.faction

        self._score()

        for instance in Session.query(Instance).all():
            data = bosses[instance.name(c.faction)] = {'useful_drops': {}, 'useful': 0, 'value': 0}
            for boss in instance.bosses:
                for drop in boss.drops:
                    utility = c.character.drop_utility(drop)
                    if utility > 0:
                        data['value'] = data['value'] + utility
                        data['useful'] = data['useful'] + 1

                        useful_bosses = data['useful_drops']
                        order = boss.order
                        useful_bosses.setdefault(order, []).append(drop)

        c.advice_rows = []

        for instance in sorted(bosses.values(), key=itemgetter('value'), reverse=True):
            first_in_instance = True
            for boss_order in sorted(instance['useful_drops'].keys()):
                boss = instance['useful_drops'][boss_order]
                first_in_boss = True
                for drop in boss:
                    row = {'drop': drop}
                    if first_in_instance:
                        row['instance_rowspan'] = instance['useful']
                    if first_in_boss:
                        row['boss_rowspan'] = len(boss)
                    first_in_instance = False
                    first_in_boss = False
                    c.advice_rows.append(row)
                    
