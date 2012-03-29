from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, String, Boolean

from raidgear.model.meta import Base

class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    instance_id = Column(Integer, ForeignKey('instance.id'))
    mode_id = Column(Integer, ForeignKey('mode.id'))

    faction_id = Column(Integer, ForeignKey('faction.id'))
    faction = relationship('Faction', backref='groups')
    
    instance = relationship('Instance')
    mode = relationship('Mode')

    def __init__(self, instance, mode):
        self.instance = instance
        self.mode = mode

    def __repr__(self):
        return "<Group %s %s>" % (self.instance.republic_name, self.mode.name)

class Instance(Base):
    __tablename__ = "instance"

    id = Column(Integer, primary_key=True)
    republic_name = Column(String(64), unique=True)
    empire_name = Column(String(64), unique=True)

    def __init__(self, republic_name, empire_name=None):
        if empire_name is None:
            empire_name = republic_name
        self.republic_name = republic_name
        self.empire_name = empire_name

    def name(self, faction):
        if faction.name == 'Republic':
            return self.republic_name
        else:
            return self.empire_name

    def __repr__(self):
        return "<Instance %s>" % self.republic_name

class Boss(Base):
    __tablename__ = "boss"

    id = Column(Integer, primary_key=True)
    order = Column(Integer)

    instance_id = Column(Integer, ForeignKey('instance.id'))
    instance = relationship('Instance', backref=backref('bosses'))
    
    republic_name = Column(String(64))
    empire_name = Column(String(64))

    def __init__(self, order, instance, republic_name, empire_name=''):
        if empire_name == '':
            empire_name = republic_name
        self.order = order
        self.instance = instance
        self.republic_name = republic_name
        self.empire_name = empire_name

    def name(self, faction):
        if faction.name == 'Republic':
            return self.republic_name
        else:
            return self.empire_name

    def describe(self, faction):
        return '%s: #%d %s' % (self.instance.name(faction), self.order, self.name(faction))

class Mode(Base):
    __tablename__ = "mode"

    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    loot_multiplier = Column(Integer)

    def __init__(self, size, loot_multiplier):
        self.size = size
        self.loot_multiplier = loot_multiplier

    def __repr__(self):
        return "<Mode %d>" % self.size
