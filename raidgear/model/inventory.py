from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, String, Boolean, Float

from raidgear.model.meta import Base, Session
from raidgear.model.gear import Gear, Drop
from raidgear.model.misc import Spec, Faction, AdvClass

class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    faction = Column(String(32))
    ready = Column(Boolean)
    
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', backref='characters')

    spec_id = Column(Integer, ForeignKey('spec.id'))
    spec = relationship('Spec', backref='characters')

    faction_id = Column(Integer, ForeignKey('faction.id'))
    faction = relationship('Faction', backref='characters')

    advclass_id = Column(Integer, ForeignKey('advclass.id'))
    advclass = relationship('AdvClass', backref='characters')

    def __init__(self, name=''):
        self.name = name
        self.faction = Session.query(Faction).filter_by(name='Republic').one()
        self.advclass = Session.query(AdvClass).order_by(AdvClass.id).first()
        self.spec = Session.query(Spec).order_by(Spec.id).first()
        self.ready = False
        for slot in Session.query(Slot).all():
            for i in xrange(0, slot.count):
                Session.add(Equipped(self, slot, i))

    def gearscore(self):
        gearscore = 0.0
        total_weight = 0.0
        for equip in Session.query(Equipped).filter_by(character=self).all():
            if equip.gear.rank < 0:
                continue
            gearscore = gearscore + equip.gear.value() * equip.slot.weight
            total_weight = total_weight + equip.slot.weight
        return gearscore / total_weight

    def drop_utility(self, drop):
        equipped = Equipped.get_all(self, drop.slot)
        utility = max(map(lambda e: drop.gear.value() - e.gear.value(), equipped))
        if utility < 0:
            utility = 0
        return utility * drop.slot.weight

    def boss_utility(self, boss):
        utility = 0.0
        for drop in boss.drops:
            utility = utility + self.drop_utility(drop)
        return utility

    def instance_utility(self, instance):
        utility = 0.0
        for boss in instance.bosses:
            utility = utility + self.boss_utility(boss)
        return utility

    def __repr__(self):
        return "<Character('%s')" % self.name

class Slot(Base):
    __tablename__ = "slot"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    count = Column(Integer)
    position = Column(Integer)
    weight = Column(Float)

    def __init__(self, name='', position=None, weight=1.0, count=1):
        self.name = name
        self.count = count
        self.position = position
        self.weight = weight

    @classmethod
    def by_name(self, name):
        return Session.query(Slot).filter_by(name=name).first()

    def __repr__(self):
        return "<Slot('%s')" % self.name

class Equipped(Base):
    __tablename__ = "equipped"

    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)
    slot_id = Column(Integer, ForeignKey('slot.id'), primary_key=True)
    gear_id = Column(Integer, ForeignKey('gear.id'))
    index = Column(Integer, primary_key=True)

    character = relationship('Character', backref=backref('equipped'))
    slot = relationship('Slot')
    gear = relationship('Gear')

    def __init__(self, character=None, slot=None, index=0):
        self.character = character
        self.slot = slot
        self.index = index
        self.gear = Session.query(Gear).filter(Gear.rank == 0).first()

    @classmethod
    def get_all(self, character, slot):
        return Session.query(Equipped).filter_by(character=character, slot=slot).all()

    def name(self):
        if self.slot.count == 1:
            return self.slot.name
        else:
            return '%s %s' % (self.slot.name, self.index + 1)

    def position(self):
        return self.slot.position + self.index

    def __repr__(self):
        return "<Equipped('%s', %s, %s)>" % (self.character.name, self.name(), self.gear.name)
