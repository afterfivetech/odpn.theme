# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from odpn.theme.testing import ODPN_THEME_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that odpn.theme is properly installed."""

    layer = ODPN_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if odpn.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'odpn.theme'))

    def test_browserlayer(self):
        """Test that IOdpnThemeLayer is registered."""
        from odpn.theme.interfaces import (
            IOdpnThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IOdpnThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = ODPN_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['odpn.theme'])

    def test_product_uninstalled(self):
        """Test if odpn.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'odpn.theme'))

    def test_browserlayer_removed(self):
        """Test that IOdpnThemeLayer is removed."""
        from odpn.theme.interfaces import IOdpnThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IOdpnThemeLayer, utils.registered_layers())
