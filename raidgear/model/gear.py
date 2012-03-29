from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, String, Boolean, Float

from raidgear.model.meta import Base, Session

class Gear(Base):
    __tablename__ = "gear"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    pvp = Column(Boolean)
    rank = Column(Float)

    def __init__(self, name='', pvp=False, rank=0):
        self.name = name
        self.pvp = pvp
        self.rank = rank

    @classmethod
    def by_name(self, name):
        return Session.query(Gear).filter_by(name=name).first()

    def describe(self):
        if self.rank < 0:
            return self.name
        elif self.pvp:
            return 'Rank %.3g (pvp): %s' % (self.rank, self.name)
        else:
            return 'Rank %.3g: %s' % (self.rank, self.name)

    def value(self):
        # Turns out that battlemaster gear is radically different for
        # various classes, no good comparison here
        
        #if self.pvp:
        #    return self.rank - 0.18
        #else:
            return self.rank

    def __repr__(self):
        return "<Gear('%s')" % self.name

class Drop(Base):
    __tablename__ = "drop"

    id = Column(Integer, primary_key=True)

    gear_id = Column(Integer, ForeignKey('gear.id'))
    boss_id = Column(Integer, ForeignKey('boss.id'))
    slot_id = Column(Integer, ForeignKey('slot.id'))

    boss = relationship('Boss', backref=backref('drops'))
    gear = relationship('Gear')
    slot = relationship('Slot')

    def __init__(self, boss, gear, slot):
        self.boss = boss
        self.gear = gear
        self.slot = slot
