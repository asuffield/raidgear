"""The application's model objects"""
from raidgear.model.meta import Session, Base

from raidgear.model.inventory import Character, Slot, Equipped
from raidgear.model.gear import Gear, Drop
from raidgear.model.raid import Group, Instance, Boss, Mode
from raidgear.model.misc import Spec, Faction, AdvClass

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
