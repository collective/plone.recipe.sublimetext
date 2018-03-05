# _*_ coding: utf-8 _*_
""" """
from zc.buildout import UserError

import json
import logging
import os
import re
import sys
import zc.recipe.egg


PY2 = sys.version_info[0] == 2

json_comment = re.compile(r'/\*.*?\*/', re.DOTALL | re.MULTILINE)
json_dump_params = {
    'sort_keys': True,
    'indent': 4,
    'separators': (',', ':'),
}
json_load_params = {}

default_st3_folders_settings = [
    {
        'path': '.',
        'follow_symlinks': 'true',
        'folder_exclude_patterns': [
            'bin',
            'develop-eggs',
            'eggs',
            'include',
            'lib',
            'local',
            'parts',
            'var',
            '.sass-cache',
            '.yolk',
        ],
    },
    {
        'path': 'parts/omelette',
        'follow_symlinks': 'true',
    },
]

if PY2:
    json_dump_params['encoding'] = 'utf-8'
    json_load_params['encoding'] = 'utf-8'


class Recipe:

    """zc.buildout recipe for sublimetext project settings:
    """

    def __init__(self, buildout, name, options):
        """ """
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(self.name)

        self.egg = zc.recipe.egg.Egg(buildout, self.options['recipe'], options)

        self._set_defaults()

        develop_eggs = []

        if self.options['ignore-develop'].lower() in ('yes', 'true', 'on', '1', 'sure'):

            develop_eggs = os.listdir(buildout['buildout']['develop-eggs-directory'])
            develop_eggs = [dev_egg[:-9] for dev_egg in develop_eggs]

        ignores = options.get('ignores', '').split()
        self.ignored_eggs = develop_eggs + ignores

        self.packages = [
            l.strip()
            for l in self.options['packages'].splitlines()
            if l.strip()]

    def install(self):
        """Let's build sublimetext project file:
        This is the method will be called by buildout it-self and this recipe
        will generate or/update sublime project file (*.sublime-project) based
        on provided options.
        """
        options = self.normalize_options()

        location = options['location']
        if not os.path.exists(location):
            os.mkdir(location)
        eggs_locations = set()
        develop_eggs_locations = set()
        develop_eggs = os.listdir(self.buildout['buildout']['develop-eggs-directory'])
        develop_eggs = [dev_egg[:-9] for dev_egg in develop_eggs]

        try:
            requirements, ws = self.egg.working_set()

            for dist in ws.by_key.values():

                project_name = dist.project_name
                if project_name not in self.ignored_eggs:
                    eggs_locations.add(dist.location)
                if project_name in develop_eggs:
                    develop_eggs_locations.add(dist.location)

            for package in self.packages:
                eggs_locations.add(package)

        except Exception as exc:
            raise UserError(str(exc))

        st3_settings = self._prepare_settings(list(eggs_locations), list(develop_eggs_locations))
        project_file = os.path.join(
            options['location'],
            options['project-name'] + '.sublime-project',
        )

        self._write_project_file(project_file, st3_settings, options['overwrite'])

        return project_file

    update = install

    def normalize_options(self):
        """This method is simply doing tranformation of cfg string to python datatype.
        For example: yes(cfg) = True(python), 2(cfg) = 2(python)"""

        # Check for required and optional options
        options = self.options.copy()

        options['overwrite'] = self.options['overwrite'].lower() in ('yes', 'true', 'on', '1', 'sure')
        options['jedi-enabled'] = self.options['jedi-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['jedi-use-omelette'] = self.options['jedi-use-omelette'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['sublimelinter-enabled'] = self.options['sublimelinter-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['sublimelinter-pylint-enabled'] = self.options['sublimelinter-pylint-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['sublimelinter-flake8-enabled'] = self.options['sublimelinter-flake8-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')

        # Anaconda settings
        options['anaconda-enabled'] = self.options['anaconda-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['anaconda-linting-enabled'] = self.options['anaconda-linting-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['anaconda-completion-enabled'] = self.options['anaconda-completion-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['anaconda-pylint-enabled'] = self.options['anaconda-pylint-enabled'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')
        options['anaconda-validate-imports'] = self.options['anaconda-validate-imports'].lower() in\
            ('yes', 'true', 'on', '1', 'sure')

        return options

    def _set_defaults(self):
        """This is setting default values of all possible options"""

        self.options.setdefault('location', self.buildout['buildout']['directory'])

        def guess_project_name():

            project_name = ''
            for root, dirs, files in os.walk(self.options['location']):
                for file in files:
                    if file.endswith('.sublime-project'):
                        project_name = '.'.join(file.split('.')[:-1])
                        break
            if not project_name:
                # No existing project file/name is exists
                # Let's make buildout directoy as project name
                project_name = self.options['location'].split('/')[-1]
            return project_name

        self.options.setdefault('project-name', guess_project_name())
        self.options.setdefault('overwrite', 'False')
        self.options.setdefault('jedi-enabled', 'False')
        self.options.setdefault('jedi-use-omelette', 'False')
        self.options.setdefault('omelette-location', os.path.join(
            self.buildout['buildout']['parts-directory'], 'omelette'),
        )
        self.options.setdefault('sublimelinter-enabled', 'False')
        self.options.setdefault('sublimelinter-pylint-enabled', 'False')
        self.options.setdefault('sublimelinter-pylint-executable', '')
        self.options.setdefault('sublimelinter-flake8-enabled', 'False')
        self.options.setdefault('sublimelinter-flake8-executable', '')
        self.options.setdefault('python-executable', str(sys.executable))

        self.options.setdefault('ignore-develop', 'False')
        self.options.setdefault('ignores', '')
        self.options.setdefault('packages', '')

        # Aanaconda Settings
        self.options.setdefault('anaconda-enabled', 'False')
        self.options.setdefault('anaconda-linting-enabled', 'True')
        self.options.setdefault('anaconda-completion-enabled', 'True')
        self.options.setdefault('anaconda-pylint-enabled', 'False')
        self.options.setdefault('anaconda-validate-imports', 'True')
        self.options.setdefault('anaconda-pep8-ignores', '')

    def _prepare_settings(self, eggs_locations, develop_eggs_locations):
        """ """
        options = self.normalize_options()
        settings = dict(settings={})

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.json'), 'r') as f:
            default_settings = json.load(f, **json_load_params)

        settings['settings'] = default_settings['ST3_DEFAULTS']
        settings['settings']['python_interpreter'] = options['python-executable']

        if options['jedi-enabled']:

            if options['jedi-use-omelette']:
                # Add the omelette and the development eggs to the jedi list.
                # This has the advantage of opening files at the omelette location,
                # keeping open files inside the project. Making it possible to
                # navigate to the location in the project, syncing the toolbar, and
                # inspecting the full module not just the individual file.
                settings['settings'].update({
                    'python_package_paths': [options['omelette-location']] + develop_eggs_locations,
                })
            else:
                # Add the paths of all eggs to the jedi list, using the absolute
                # location of the eggs (which usually is at the buildout eggs cache,
                # outside of the project).
                settings['settings'].update({
                    'python_package_paths': eggs_locations,
                })

        if options['sublimelinter-enabled']:

            self._prepare_sublinter_settings(settings, default_settings, eggs_locations, options)

        if options['anaconda-enabled']:

            self._prepare_anaconda_settings(settings, default_settings, eggs_locations, options)

        return settings

    def _prepare_anaconda_settings(self, settings, default_settings, eggs_locations, options):
        """All anaconda specific settings are handled by this method."""

        default_anaconda_settings = default_settings['ANACONDA_DEFAULTS']
        settings['build_systems'] = default_anaconda_settings['build_systems']

        settings['build_systems'][0].update({
            'shell_cmd': '{project_path}/bin/python -u "$file"'.format(
                project_path=self.buildout['buildout']['directory']),
        })

        settings['settings'].update(default_anaconda_settings['settings'])

        settings['settings'].update({
            'validate_imports': options['anaconda-validate-imports'],
            'disable_anaconda_completion': not options['anaconda-completion-enabled'],
            'anaconda_linting': options['anaconda-linting-enabled'],
            'use_pylint': options['anaconda-pylint-enabled'],
            'extra_paths': eggs_locations,
        })
        if options['anaconda-pep8-ignores']:
            settings['settings'].update({
                'pep8_ignore': options['anaconda-pep8-ignores'].split(),
            })

    def _prepare_sublinter_settings(self, settings, default_settings, eggs_locations, options):
        """All sublinter related settings are done by this method."""

        settings['settings'].update({'sublimelinter': True})

        settings['SublimeLinter'] = default_settings['SUBLIMELINTER_DEFAULTS']

        # Now check for flake8
        if options['sublimelinter-flake8-enabled']:

            settings['SublimeLinter']['linters']['flake8'] =\
                default_settings['SUBLIMELINTER_FLAKE8_DEFAULTS']

            if options['sublimelinter-flake8-executable']:
                exc_path = options['sublimelinter-flake8-executable']
                settings['SublimeLinter']['linters']['flake8']['executable'] = \
                    self._resolve_executable_path(exc_path)

        # Now check for pylint
        if options['sublimelinter-pylint-enabled']:
            settings['SublimeLinter']['linters']['pylint'] =\
                default_settings['SUBLIMELINTER_PYLINTER_DEFAULTS']

            settings['SublimeLinter']['linters']['pylint'].update({
                'paths': eggs_locations,

            })
            if options['sublimelinter-pylint-executable']:
                exc_path = options['sublimelinter-pylint-executable']
                settings['SublimeLinter']['linters']['pylint']['executable'] = \
                    self._resolve_executable_path(exc_path)

    def _write_project_file(self, project_file, settings, overwrite=False):
        """Project File Writer:
        This method is actual doing writting project file to file system."""
        try:
            if not overwrite and os.path.exists(project_file):
                with open(project_file, 'r') as f:
                    # get comment cleaned (/* */) json string
                    json_string = json_comment.sub('', f.read().strip())
                    existing_st3_settings = json.loads(json_string, **json_load_params)

                    if existing_st3_settings:
                        self._merge_settings(settings, existing_st3_settings)
                        settings = existing_st3_settings.copy()

            if 'folders' not in settings:
                settings['folders'] = default_st3_folders_settings

            with open(project_file, 'w') as f:
                self.logger.info('Generate sublimetext project at `{0}`.'.format(project_file))
                json.dump(settings, f, **json_dump_params)

        except ValueError as exc:
            # catching any json error
            raise UserError(str(exc))

    def _merge_settings(self, new_settings, existing_settings):
        """Respect Existing Settings:
        Depends on overwrite option, this method is intelligently respect/keep
        any existing settings, only replace if value affected by buildout options."""

        for key, value in new_settings.items():

            try:
                item = existing_settings[key]
                if isinstance(value, dict) and (type(item) == type(value)):
                    self._merge_settings(value, item)
                    existing_settings[key] = item
                else:
                    existing_settings[key] = value

            except KeyError:
                # New Item
                existing_settings[key] = value

    def _resolve_executable_path(self, path_):
        """ """
        # Noramalized Path on demand
        if path_.startswith('~'):
            path_ = os.path.expanduser(path_)

        elif path_.startswith('./'):
            path_ = path_.replace('.', self.buildout['buildout']['directory'])

        elif path_.startswith('${buildout:directory}'):
            path_ = path_.replace('${buildout:directory}', self.buildout['buildout']['directory'])

        elif path_.startswith('$project_path/'):
            path_ = path_.replace('$project_path', self.buildout['buildout']['directory'])

        return path_


def uninstall(name, options):
    """Nothing much need to do with uninstall, because this recipe is doing so much filesystem writting.
    Depends overwrite option, generated project file is removed."""

    logger = logging.getLogger(name)
    logger.info('uninstalling ...')

    if options.get('overwrite', 'False').lower() in ('yes', 'true', 'on', '1', 'sure'):
        project_file = os.path.join(options['location'], options['project-name'] + '.sublime-project')
        logger.info('removed generated file /{0}'.format(project_file.split('/')[-1]))
        os.unlink(project_file)
