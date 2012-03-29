"""Setup the raidgear application"""
import logging

import pylons.test

from raidgear.config.environment import load_environment
from raidgear.model.meta import Session, Base

from raidgear.model import Slot, Gear, Boss, Drop, Instance, Mode, Spec, Faction, AdvClass

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup raidgear here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.drop_all(bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

    republic = Faction('Republic')
    Session.add(republic)
    empire = Faction('Empire')
    Session.add(empire)

    Session.add(AdvClass(republic, 'Guardian'))
    Session.add(AdvClass(republic, 'Sentinel'))
    Session.add(AdvClass(republic, 'Sage'))
    Session.add(AdvClass(republic, 'Shadow'))
    Session.add(AdvClass(republic, 'Commando'))
    Session.add(AdvClass(republic, 'Vanguard'))
    Session.add(AdvClass(republic, 'Scoundrel'))
    Session.add(AdvClass(republic, 'Gunslinger'))

    Session.add(AdvClass(empire, 'Marauder'))
    Session.add(AdvClass(empire, 'Juggernaut'))
    Session.add(AdvClass(empire, 'Sorcerer'))
    Session.add(AdvClass(empire, 'Assassin'))
    Session.add(AdvClass(empire, 'Mercenary'))
    Session.add(AdvClass(empire, 'Powertech'))
    Session.add(AdvClass(empire, 'Sniper'))
    Session.add(AdvClass(empire, 'Operative'))

    # Add the basic fields
    head = Slot('Head', 9, 0.0897)
    chest = Slot('Chest', 10, 0.0818)
    gloves = Slot('Gloves', 11, 0.0897)
    belt = Slot('Belt', 12, 0.0628)
    legs = Slot('Legs', 13, 0.0897)
    boots = Slot('Boots', 14, 0.0818)
    ear = Slot('Ear', 1, 0.0743)
    implant = Slot('Implant', 2, 0.07232, 2)
    bracers = Slot('Bracers', 4, 0.0687)
    relic = Slot('Relic', 5, 0.0304, 2)
    mainhand = Slot('Mainhand', 7, 0.0838)
    offhand = Slot('Offhand', 8, 0.0723)
    Session.add_all([head, chest, belt, legs, boots, ear, implant, relic, mainhand, offhand])

    # Not actually in game
    #Session.add(Gear('Unavailable', rank=-1))
    weak = Gear('Blues or worse', rank=0)
    Session.add(weak)
    purple = Gear('Generic purple at 49+', rank=1)
    Session.add(purple)
    Session.add(Gear('Centurion', rank=2, pvp=True))
    xenotech = Gear('Xenotech', rank=2)
    Session.add(xenotech)
    energized = Gear('Energized', rank=2)
    Session.add(energized)
    tionese = Gear('Tionese', rank=2)
    Session.add(tionese)
    Session.add(Gear('Champion', rank=3, pvp=True))
    columi = Gear('Columi', rank=3)
    Session.add(columi)
    exotech = Gear('Exotech', rank=3)
    Session.add(exotech)
    rakata = Gear('Rakata', rank=4)
    Session.add(rakata)
    Session.add(Gear('Battlemaster', rank=4, pvp=True))
    Session.add(Gear('Matrix cube at 50', rank=4))

    esseles_instance = Instance('Esseles', 'Black Talon')

    esseles = [
        Boss(1, esseles_instance, 'Lieutenant Isric', 'GXR-5 Sabotage Droid'),
        Boss(2, esseles_instance, 'Ironfist', 'Commander Ghulil'),
        Boss(3, esseles_instance, 'ISS-994 Power Droid', 'GXR-7 Command Droid'),
        Boss(4, esseles_instance, 'Vokk', 'Yadira Ban'),
        ]

    Session.add_all(esseles)
    Session.add(Drop(esseles[0], tionese, belt))
    Session.add(Drop(esseles[1], energized, legs))
    Session.add(Drop(esseles[2], tionese, ear))
    Session.add(Drop(esseles[3], columi, bracers))

    emperor_instance = Instance('False Emperor')

    emperor = [
        Boss(1, emperor_instance, 'Jindo Krey'),
        Boss(2, emperor_instance, 'HK-47'),
        Boss(3, emperor_instance, 'Sith Entity'),
        Boss(4, emperor_instance, 'Darth Malgus'),
        ]

    Session.add_all(emperor)
    Session.add(Drop(emperor[0], tionese, gloves))
    Session.add(Drop(emperor[1], tionese, mainhand))
    Session.add(Drop(emperor[2], tionese, implant))
    Session.add(Drop(emperor[3], columi, chest))

    directive7_instance = Instance('Directive 7')

    directive7 = [
        Boss(1, directive7_instance, 'Interrogator'),
        Boss(2, directive7_instance, 'Bulwark'),
        Boss(3, directive7_instance, 'Replicator'),
        Boss(4, directive7_instance, 'Mentor'),
        ]

    Session.add_all(directive7)
    Session.add(Drop(directive7[0], tionese, bracers))
    Session.add(Drop(directive7[1], energized, chest))
    Session.add(Drop(directive7[2], purple, relic))
    Session.add(Drop(directive7[3], columi, legs))

    ilum_instance = Instance('Battle of Ilum')

    ilum = [
        Boss(1, ilum_instance, 'Velasu & Drinda'),
        Boss(2, ilum_instance, 'Krel Thak'),
        Boss(3, ilum_instance, 'Guid Patriach'),
        Boss(4, ilum_instance, 'Darth Serevin'),
        ]

    Session.add_all(ilum)
    Session.add(Drop(ilum[0], tionese, bracers))
    Session.add(Drop(ilum[1], energized, head))
    Session.add(Drop(ilum[2], tionese, ear))
    Session.add(Drop(ilum[3], columi, offhand))

    taral5_instance = Instance('Taral V', 'Boarding Party')

    taral5 = [
        Boss(1, taral5_instance, 'Handler Gattan', 'HXI-54'),
        Boss(2, taral5_instance, 'Ripper', "Sakan Do'nair"),
        Boss(3, taral5_instance, 'Lord Hasper', 'Engineer Kels'),
        Boss(4, taral5_instance, 'General Edikar', 'Jorland'),
        ]

    Session.add_all(taral5)
    Session.add(Drop(taral5[0], purple, relic))
    Session.add(Drop(taral5[1], energized, boots))
    Session.add(Drop(taral5[2], tionese, implant))
    Session.add(Drop(taral5[3], columi, gloves))

    maelstrom_instance = Instance('Maelstrom Prison', 'The Foundry')
    
    maelstrom = [
        Boss(1, maelstrom_instance, '', 'Foundry Guardian'),
        Boss(2, maelstrom_instance, '', 'HK-47'),
        Boss(3, maelstrom_instance, '', 'Borrower Matriarch'),
        Boss(4, maelstrom_instance, 'Grand Moff Kilran', 'Revan'),
        ]

    Session.add_all(maelstrom)
    Session.add(Drop(maelstrom[0], tionese, boots))
    Session.add(Drop(maelstrom[1], tionese, offhand))
    Session.add(Drop(maelstrom[2], tionese, belt))
    Session.add(Drop(maelstrom[3], columi, boots))

    kaon_instance = Instance('Kaon Under Siege')

    kaon = [
        Boss(1, kaon_instance, 'Defend vs Zombie'),
        Boss(2, kaon_instance, 'Rakghoul Behemoth'),
        Boss(3, kaon_instance, 'KR-82 Expulser'),
        Boss(4, kaon_instance, "Commander Lk'Graagth"),
        ]

    Session.add_all(kaon)
    Session.add(Drop(kaon[0], xenotech, gloves))
    Session.add(Drop(kaon[1], tionese, mainhand))
    Session.add(Drop(kaon[2], columi, head))
    Session.add(Drop(kaon[3], columi, head))

    ev_normal_instance = Instance('Eternity Vault (normal)')

    ev = [
        Boss(1, ev_normal_instance, 'Annihilation Droid XRR-3'),
        Boss(2, ev_normal_instance, 'Gharj'),
        Boss(3, ev_normal_instance, 'Ancient Pylons'),
        Boss(4, ev_normal_instance, 'Infernal Council'),
        Boss(5, ev_normal_instance, 'Soa'),
        ]

    Session.add_all(ev)
    Session.add(Drop(ev[0], energized, head))
    Session.add(Drop(ev[0], columi, gloves))
    Session.add(Drop(ev[1], tionese, belt))
    Session.add(Drop(ev[1], columi, offhand))
    Session.add(Drop(ev[2], columi, legs))
    Session.add(Drop(ev[2], tionese, bracers))
    Session.add(Drop(ev[3], columi, boots))
    Session.add(Drop(ev[3], tionese, relic))
    Session.add(Drop(ev[4], columi, chest))
    Session.add(Drop(ev[4], tionese, mainhand))

    ev_hard_instance = Instance('Eternity Vault (hard)')

    ev_hard = [
        Boss(1, ev_hard_instance, 'Annihilation Droid XRR-3'),
        Boss(2, ev_hard_instance, 'Gharj'),
        Boss(3, ev_hard_instance, 'Ancient Pylons'),
        Boss(4, ev_hard_instance, 'Infernal Council'),
        Boss(5, ev_hard_instance, 'Soa'),
        ]

    Session.add_all(ev_hard)
    Session.add(Drop(ev_hard[0], exotech, head))
    Session.add(Drop(ev_hard[0], rakata, gloves))
    Session.add(Drop(ev_hard[1], columi, belt))
    Session.add(Drop(ev_hard[1], rakata, offhand))
    Session.add(Drop(ev_hard[1], columi, implant))
    Session.add(Drop(ev_hard[2], rakata, legs))
    Session.add(Drop(ev_hard[2], columi, bracers))
    Session.add(Drop(ev_hard[3], rakata, boots))
    Session.add(Drop(ev_hard[3], columi, relic))
    Session.add(Drop(ev_hard[4], rakata, chest))
    Session.add(Drop(ev_hard[4], columi, mainhand))

    kp_instance = Instance("Karagga's Palace (normal)")

    kp = [
        Boss(1, kp_instance, 'Bonethrasher'),
        Boss(2, kp_instance, 'Jarg & Sorno'),
        Boss(3, kp_instance, 'Foreman Crusher'),
        Boss(4, kp_instance, 'G4-B3 Fabricator'),
        Boss(5, kp_instance, 'Karagga the Fatty'),
        ]

    Session.add_all(kp)
    Session.add(Drop(kp[0], columi, head))
    Session.add(Drop(kp[0], xenotech, gloves))
    Session.add(Drop(kp[1], columi, belt))
    Session.add(Drop(kp[1], tionese, offhand))
    Session.add(Drop(kp[2], xenotech, legs))
    Session.add(Drop(kp[2], columi, bracers))
    Session.add(Drop(kp[3], xenotech, boots))
    Session.add(Drop(kp[3], columi, relic))
    Session.add(Drop(kp[4], xenotech, chest))
    Session.add(Drop(kp[4], columi, mainhand))

    kp_hard_instance = Instance("Karagga's Palace (hard)")

    kp_hard = [
        Boss(1, kp_hard_instance, 'Bonethrasher'),
        Boss(2, kp_hard_instance, 'Jarg & Sorno'),
        Boss(3, kp_hard_instance, 'Foreman Crusher'),
        Boss(4, kp_hard_instance, 'G4-B3 Fabricator'),
        Boss(5, kp_hard_instance, 'Karagga the Fatty'),
        ]

    Session.add_all(kp_hard)
    Session.add(Drop(kp_hard[0], rakata, head))
    Session.add(Drop(kp_hard[0], exotech, gloves))
    Session.add(Drop(kp_hard[1], rakata, belt))
    Session.add(Drop(kp_hard[1], columi, offhand))
    Session.add(Drop(kp_hard[2], exotech, legs))
    Session.add(Drop(kp_hard[2], rakata, bracers))
    Session.add(Drop(kp_hard[3], exotech, boots))
    Session.add(Drop(kp_hard[3], rakata, relic))
    Session.add(Drop(kp_hard[4], exotech, chest))
    Session.add(Drop(kp_hard[4], rakata, mainhand))

    Session.add(Mode(4, 1))
    Session.add(Mode(8, 2))
    Session.add(Mode(16, 4))

    Session.add(Spec('Melee DPS', 'melee'))
    Session.add(Spec('Ranged DPS', 'ranged'))
    Session.add(Spec('Heal', 'healing'))
    Session.add(Spec('Tank', 'tank'))

    Session.commit()
