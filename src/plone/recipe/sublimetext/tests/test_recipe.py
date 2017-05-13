# _*_ coding: utf-8 _*_
from zc.buildout import rmtree
from zc.buildout.testing import Buildout

import os
import tempfile
import unittest


class TestRecipe(unittest.TestCase):
    """ """
    def setUp(self):

        self.here = os.getcwd()

        self.location = tempfile.mkdtemp(prefix='plone.recipe.sublimetext')
        os.chdir(self.location)

        self.buildout = buildout = Buildout()
        # Set eggs
        buildout['buildout']['eggs'] = 'zope.interface'
        buildout['buildout']['buildout-directory'] = self.location
        self.recipe_options = dict(
            recipe='',
            overwrite='1',
            eggs='zope.interface'
        )
        self.recipe_options['project-name'] = 'sublimetext-recipe'

        buildout['sublimetext'] = self.recipe_options

        from ..recipes import Recipe
        self.recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])

    def test_install(self):
        """"""
        self.recipe.install()

    def test__prepare_settings(self):
        """ """
        test_eggs_locations = [
            '/tmp/eggs/egg1.egg',
            '/tmp/eggs/egg2.egg'
        ]
        settings = self.recipe._prepare_settings(test_eggs_locations)

    def tearDown(self):
        os.chdir(self.here)
        rmtree.rmtree(self.location)
