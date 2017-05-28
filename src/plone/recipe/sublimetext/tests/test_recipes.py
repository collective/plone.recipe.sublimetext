# _*_ coding: utf-8 _*_
from zc.buildout import rmtree
from zc.buildout import UserError
from zc.buildout.testing import Buildout
from zc.buildout.testing import mkdir
from zc.buildout.testing import read
from zc.buildout.testing import write

import json
import os
import tempfile
import unittest


JSON_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'template.json')
TEST_DIR = os.path.abspath(os.path.dirname(__file__))


class TestRecipe(unittest.TestCase):
    """ """
    def setUp(self):

        self.here = os.getcwd()

        self.location = tempfile.mkdtemp(prefix='plone.recipe.sublimetext')
        mkdir(self.location, 'develop-eggs')
        os.chdir(self.location)

        self.buildout = Buildout()
        # Set eggs
        self.buildout['buildout']['directory'] = self.location

        self.recipe_options = dict(
            recipe='plone.recipe.sublimetext',
            overwrite='False',
            eggs='zc.recipe.egg\nzc.buildout'
        )
        self.recipe_options['project-name'] = 'sublimetext-recipe'

    def test_install(self):
        """"""
        from ..recipes import Recipe

        buildout = self.buildout
        recipe_options = self.recipe_options.copy()
        recipe_options.update({
            'jedi-enabled': '1',
            'sublimelinter-enabled': '1',
            'sublimelinter-pylint-enabled': 'True',
            'anaconda-enabled': 'True'
        })
        buildout['sublimetext'] = recipe_options
        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        recipe.install()

        generated_settings = json.loads(
            read(os.path.join(self.location, recipe_options['project-name'] + '.sublime-project'))
        )
        # should be three, zc.buildout, zc,recipe.egg, python site-package path
        self.assertEqual(3, len(generated_settings['settings']['python_package_paths']))
        self.assertEqual(3, len(generated_settings['settings']['extra_paths']))
        self.assertIn(
            recipe.buildout['buildout']['directory'] + '/bin/python',
            generated_settings['build_systems'][0]['shell_cmd']
        )

        # Test with custom location with package
        buildout['sublimetext'].update({
            'packages': '/fake/path',
            'location': os.path.join(tempfile.gettempdir(), 'hshdshgdrts')
        })

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        recipe.install()

        generated_settings = json.loads(
            read(os.path.join(
                buildout['sublimetext']['location'],
                recipe_options['project-name'] + '.sublime-project'
            ))
        )

        # Now should four links
        self.assertEqual(4, len(generated_settings['settings']['python_package_paths']))

        # Make sure settings file is created at custom location
        self.assertTrue(os.path.exists(os.path.join(
            buildout['sublimetext']['location'],
            buildout['sublimetext']['project-name'] + '.sublime-project'
        )))

        # restore
        rmtree.rmtree(buildout['sublimetext']['location'])
        del buildout['sublimetext']['location']
        del buildout['sublimetext']['packages']

        # Test ignores
        buildout['buildout'].update({
            'develop': '.'
        })
        buildout['sublimetext'].update({
            'ignores': 'zc.buildout',
            'ignore-develop': 'True',
        })
        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        recipe.install()

        generated_settings = json.loads(
            read(os.path.join(self.location, recipe_options['project-name'] + '.sublime-project'))
        )

        # should be two, zc.buildout is ignored
        self.assertEqual(2, len(generated_settings['settings']['python_package_paths']))

        # Failed Test: existing project file with invalid json
        write(
            self.location,
            recipe_options['project-name'] + '.sublime-project',
            """I am invalid"""
        )
        try:
            recipe.update()
            raise AssertionError(
                'Code should not come here, as invalid json inside existing project'
                'file! ValueError raised by UserError'
            )
        except UserError:
            pass

        # Failed Test: exception rasied by zc.recipe.Egg
        recipe.options.update({
            # Invalid Egg
            'eggs': '\\'
        })
        try:
            recipe.install()
            raise AssertionError('Code should not come here, as should raised execption because of invalied eggs')
        except UserError:
            pass

    def test__set_defaults(self):
        """ """
        from ..recipes import Recipe
        buildout = self.buildout
        recipe_options = self.recipe_options.copy()

        del recipe_options['project-name']

        buildout['sublimetext'] = recipe_options
        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])

        recipe._set_defaults()
        # Test: default project name should be buildout directory name
        self.assertEqual(
            recipe.options['project-name'],
            self.location.split('/')[-1]
        )

        # Test: if any ``sublime-project`` suffix file is available inside buildout directory
        # that should be picked as default project file name
        _project_file = 'human_project'
        write(self.location, _project_file + '.sublime-project', '''[]''')
        # clear previously assaigned default
        del buildout['sublimetext']['project-name']

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        recipe._set_defaults()

        self.assertEqual(recipe.options['project-name'], _project_file)

    def test__prepare_settings(self):
        """ """
        from ..recipes import Recipe

        buildout = self.buildout
        recipe_options = self.recipe_options.copy()

        buildout['sublimetext'] = recipe_options
        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])

        test_eggs_locations = [
            '/tmp/eggs/egg1.egg',
            '/tmp/eggs/egg2.egg'
        ]

        st3_settings = recipe._prepare_settings(test_eggs_locations)

        # By Default Sublimelinter is not enabled
        self.assertFalse(st3_settings['settings']['sublimelinter'])
        self.assertNotIn('SublimeLinter', st3_settings)

        # Anaconda is not enabled as well
        self.assertNotIn('build_systems', st3_settings)
        self.assertNotIn('extra_paths', st3_settings['settings'])

        recipe_options['jedi-enabled'] = 'True'
        recipe_options['sublimelinter-enabled'] = 'True'
        recipe_options['sublimelinter-pylint-enabled'] = 'True'
        recipe_options['sublimelinter-flake8-enabled'] = 'True'
        recipe_options['sublimelinter-flake8-executable'] = '/fake/path/flake8'
        recipe_options['anaconda-enabled'] = 'True'
        recipe_options['anaconda-pylint-enabled'] = 'True'
        recipe_options['anaconda-pep8-ignores'] = 'N802\nW291'

        buildout['sublimetext'].update(recipe_options)

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        st3_settings = recipe._prepare_settings(test_eggs_locations)

        self.assertTrue(st3_settings['settings']['sublimelinter'])
        self.assertIn('SublimeLinter', st3_settings)
        self.assertEqual(test_eggs_locations, st3_settings['settings']['python_package_paths'])
        self.assertFalse(st3_settings['SublimeLinter']['linters']['pylint']['@disable'])

        # Test Anaconda Settings are avialable
        self.assertIn('build_systems', st3_settings)
        self.assertTrue(st3_settings['settings']['anaconda_linting'])
        self.assertTrue(st3_settings['settings']['use_pylint'])
        self.assertEqual(len(st3_settings['settings']['pep8_ignore']), 2)
        self.assertTrue(st3_settings['settings']['validate_imports'])

        # Test Parent `sublimelinter-enabled` is respected
        # We all children options of sublimelinter are enabled.
        del buildout['sublimetext']['sublimelinter-enabled']

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        st3_settings = recipe._prepare_settings(test_eggs_locations)
        self.assertNotIn('SublimeLinter', st3_settings)

    def test__write_project_file(self):
        """ """
        from ..recipes import Recipe
        from ..recipes import default_st3_folders_settings

        buildout = self.buildout
        recipe_options = self.recipe_options.copy()
        del recipe_options['overwrite']
        recipe_options.update({
            'sublimelinter-enabled': 'True',
            'sublimelinter-flake8-enabled': 'True'
        })

        _project_file = 'human_project.sublime-project'

        write(
            self.location, _project_file,
            """{
                /*
                 This is comment.
                */
                "tests": {
                    "hello": 1
                },
                "SublimeLinter": {
                    "linters": {
                        "flake8": {
                            "@disable": true,
                            "max-complexity": 10
                        }
                    }
                }

            }"""
        )

        buildout['sublimetext'] = recipe_options

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        recipe._set_defaults()

        test_eggs_locations = [
            '/tmp/eggs/egg1.egg',
            '/tmp/eggs/egg2.egg'
        ]

        st3_settings = recipe._prepare_settings(test_eggs_locations)
        recipe._write_project_file(
            os.path.join(self.location, _project_file),
            st3_settings,
            False
        )
        # By default no overwrite configuration, means existing configuration should be
        # available
        generated_settings = json.loads(read(os.path.join(self.location, _project_file)))
        default_settings = json.loads(read(JSON_TEMPLATE))

        # Test:: merged works with new and existing

        # Make sure value changed from buildout
        self.assertFalse(generated_settings['SublimeLinter']['linters']['flake8']['@disable'])
        # Make sure other value kept intact, because that option is not handled by this recipe
        self.assertEqual(
            generated_settings['SublimeLinter']['linters']['flake8']['max-complexity'],
            10
        )
        # Test:: default folders option is added, because existing file don't have this
        self.assertEqual(
            generated_settings['folders'],
            default_st3_folders_settings
        )

        # Test: existing configuration is kept intact
        self.assertEqual(generated_settings['tests']['hello'], 1)

        buildout['sublimetext'].update({
            'sublimelinter-enabled': 'True',
            'sublimelinter-flake8-enabled': 'False',
            'sublimelinter-pylint-enabled': 'True',
            'jedi-enabled': 'True'
        })

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        st3_settings = recipe._prepare_settings(test_eggs_locations)

        recipe._write_project_file(
            os.path.join(self.location, _project_file),
            st3_settings,
            False
        )

        generated_settings = json.loads(read(os.path.join(self.location, _project_file)))

        self.assertNotEqual(generated_settings['settings'], default_settings['ST3_DEFAULTS'])
        self.assertEqual(test_eggs_locations, generated_settings['settings']['python_package_paths'])
        self.assertIn('SublimeLinter', generated_settings)
        # Test paths are added for `pylint`
        self.assertEqual(2, len(generated_settings['SublimeLinter']['linters']['pylint']['paths']))

        # Test: overwrite works!
        recipe._write_project_file(
            os.path.join(self.location, _project_file),
            st3_settings,
            True
        )
        generated_settings = json.loads(read(os.path.join(self.location, _project_file)))
        self.assertNotIn('tests', generated_settings)
        # Test:: default folders setting
        # As completly overwrite file, so there is no folders option, so should have default
        self.assertEqual(
            generated_settings['folders'],
            default_st3_folders_settings
        )

        # Test: Anaconda Settings is working

        buildout['sublimetext'].update({
            'anaconda-enabled': 'True',
            'anaconda-pep8-ignores': 'N802 W291'
        })

        recipe = Recipe(buildout, 'sublimetext', buildout['sublimetext'])
        st3_settings = recipe._prepare_settings(test_eggs_locations)

        recipe._write_project_file(
            os.path.join(self.location, _project_file),
            st3_settings,
            True
        )

        generated_settings = json.loads(read(os.path.join(self.location, _project_file)))
        self.assertIn('build_systems', generated_settings)
        self.assertEqual(generated_settings['build_systems'][0]['name'], 'PRS:: Anaconda Python Builder')
        # By default pylint disabled
        self.assertFalse(generated_settings['settings']['use_pylint'])
        # Should have two eggs paths in `extra_paths`
        self.assertEqual(len(generated_settings['settings']['extra_paths']), 2)

    def tearDown(self):
        os.chdir(self.here)
        rmtree.rmtree(self.location)


class TestRecipeUninstall(unittest.TestCase):
    """ """
    def setUp(self):

        self.here = os.getcwd()

        self.location = tempfile.mkdtemp(prefix='plone.recipe.sublimetext')
        os.chdir(self.location)

        self.buildout = Buildout()
        # Set eggs
        self.buildout['buildout']['directory'] = self.location

        self.recipe_options = dict(
            recipe='plone.recipe.sublimetext',
            overwrite='False'
        )
        self.recipe_options['project-name'] = 'sublimetext-recipe'

    def test_uninstall(self):
        """ """
        from ..recipes import Recipe
        from ..recipes import uninstall

        recipe_options = self.recipe_options.copy()
        self.buildout['sublimetext'] = recipe_options

        recipe = Recipe(self.buildout, 'sublimetext', self.buildout['sublimetext'])
        recipe._set_defaults()

        # Test: in case of overwrite false, project file should not be removed
        filename = recipe.options['project-name'] + '.sublime-project'
        write(
            self.location,
            filename,
            '''{"hello": "T20"}'''
        )
        uninstall(recipe.name, recipe.options)

        # should be exists
        self.assertTrue(os.path.exists(filename))

        # update to overwrite True
        recipe.options.update({'overwrite': 'True'})
        uninstall(recipe.name, recipe.options)

        # now should be removed
        self.assertFalse(os.path.exists(filename))

    def tearDown(self):
        os.chdir(self.here)
        rmtree.rmtree(self.location)
