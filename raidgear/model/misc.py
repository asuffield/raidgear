from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Integer, String, Boolean, Float

from raidgear.model.meta import Base, Session

class Spec(Base):
    __tablename__ = "spec"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    css_class = Column(String(32), unique=True)

    def __init__(self, name, css_class):
        self.name = name
        self.css_class = css_class

    def __repr__(self):
        return "<Spec %s>" % self.name

class Faction(Base):
    __tablename__ = "faction"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Faction %s>" % self.name

class AdvClass(Base):
    __tablename__ = "advclass"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)

    faction_id = Column(Integer, ForeignKey('faction.id'))
    faction = relationship('Faction', backref='advclasses')

    def __init__(self, faction, name):
        self.faction = faction
        self.name = name

    def __repr__(self):
        return "<AdvClass %s>" % self.name
