# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import odpn.theme


class OdpnThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=odpn.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'odpn.theme:default')


ODPN_THEME_FIXTURE = OdpnThemeLayer()


ODPN_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ODPN_THEME_FIXTURE,),
    name='OdpnThemeLayer:IntegrationTesting'
)


ODPN_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ODPN_THEME_FIXTURE,),
    name='OdpnThemeLayer:FunctionalTesting'
)


ODPN_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ODPN_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='OdpnThemeLayer:AcceptanceTesting'
)
