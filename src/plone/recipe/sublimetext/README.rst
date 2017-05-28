Example Usage
=============

Minimal buildout::
    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... develop = .
    ... eggs =
    ...     zc.buildout
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... project-name = plone-recipe-sublime
    ... eggs = ${buildout:eggs}
    ... jedi-enabled = True
    ... """)
    >>> system(buildout + ' -c buildout.cfg')
    >>> import os
    >>> os.path.exists('plone-recipe-sublime.sublime-project')
    True

Standard buildout::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... develop = .
    ... eggs =
    ...     zc.buildout
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... project-name = plone-recipe-sublime
    ... eggs = ${buildout:eggs}
    ... jedi-enabled = True
    ... sublimelinter-enabled = True
    ... sublimelinter-flake8-enabled = True
    ... sublimelinter-flake8-executable = ${buildout:directory}/bin/flake8
    ... """)
    >>> system(buildout + ' -c buildout.cfg')
    >>> import json
    >>> settings = json.loads(read('plone-recipe-sublime.sublime-project'))
    >>> 'flake8' in settings['Sublimelinter']['linters']
    True

Muilti Linters and without project name::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... develop = .
    ... eggs =
    ...     zc.buildout
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... eggs = ${buildout:eggs}
    ... jedi-enabled = True
    ... sublimelinter-enabled = True
    ... sublimelinter-flake8-enabled = True
    ... sublimelinter-flake8-executable = ${buildout:directory}/bin/flake8
    ... sublimelinter-pylint-enabled = True
    ... """)
    >>> system(buildout + ' -c buildout.cfg')

(project filename shoul be ``plone-recipe-sublime.sublime-project`` as previously generated)::

    >>> settings = json.loads(read('plone-recipe-sublime.sublime-project'))
    >>> 'pylint' in settings['Sublimelinter']['linters']
    True

Usages Anaconda for all purpose (linting, autocompletion) and rest of all are not used::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... develop = .
    ... eggs =
    ...     zc.buildout
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... project-name = plone-recipe-sublime
    ... eggs = ${buildout:eggs}
    ... anaconda-enabled = True
    ... anaconda-pep8-ignores =
    ...     N802
    ... """)
    >>> system(buildout + ' -c buildout.cfg')
    >>> import json
    >>> settings = json.loads(read('plone-recipe-sublime.sublime-project'))
    >>> 'build_systems' in settings.keys()
    True
    >>> 'extra_paths' in settings['settings'].keys()
    True
    >>> settings['settings']['anaconda_linting']
    True
    >>> settings['settings']['use_pylint']
    False
