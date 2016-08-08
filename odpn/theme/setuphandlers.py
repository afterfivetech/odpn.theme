from collective.grok import gs
from odpn.theme import MessageFactory as _

@gs.importstep(
    name=u'odpn.theme', 
    title=_('odpn.theme import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('odpn.theme.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
