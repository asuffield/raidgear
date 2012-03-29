"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    map.connect('/', controller='menu', action='index')
    map.connect('/character', controller='menu', action='character', conditions=dict(method=['POST']))

    map.connect('/character/{charname}', controller='character', action='view')
    map.connect('/character/{charname}/equip', controller='character', action='equip', conditions=dict(method=['POST']))
    map.connect('/character/{charname}/faction', controller='character', action='faction', conditions=dict(method=['POST']))
    map.connect('/character/{charname}/ready', controller='character', action='ready', conditions=dict(method=['POST']))
    map.connect('/character/{charname}/spec', controller='character', action='spec', conditions=dict(method=['POST']))
    map.connect('/character/{charname}/advclass', controller='character', action='advclass', conditions=dict(method=['POST']))

    map.connect('/raidplan/{faction}', controller='raidplan', action='view')

    return map
