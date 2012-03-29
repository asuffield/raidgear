from paste.script.command import Command
from paste.deploy import loadapp
from raidgear.model.meta import Session, Base
from raidgear.model import Slot, Gear, Boss, Drop, Instance, Mode, Spec, Faction, AdvClass
import os

class UpdateDB(Command):
    # Parser configuration
    summary = "Update the database to reflect new data"
    usage = "update-db data.yaml"
    group_name = "raidgear"
    parser = Command.standard_parser(verbose=False)

    def command(self):
        config_file = self.args[0]
        here_dir = os.getcwd()
        config_name = 'config:%s' % config_file
        wsgiapp = loadapp(config_name, relative_to=here_dir)

        import yaml
        dataf = open(self.args[1])
        data = yaml.load(dataf.read())
        dataf.close()

        for name in data.get('slots', {}):
            slot_data = data['slots'][name]
            slot = Slot.by_name(name)
            if slot is None:
                slot = Slot(name)
                Session.add(slot)
            slot.count = int(slot_data.get('count', '1'))
            slot.weight = float(slot_data.get('weight', '1.0'))
            slot.position = int(slot_data['position'])

        for name in data.get('gear', {}):
            gear_data = data['gear'][name]
            gear = Gear.by_name(name)
            if gear is None:
                gear = Gear(name)
                Session.add(gear)
            gear.pvp = bool(gear_data.get('pvp'))
            gear.rank = float(gear_data.get('rank', '0'))

        Session.commit()
