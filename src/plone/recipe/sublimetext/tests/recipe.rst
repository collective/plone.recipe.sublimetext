plone.recipe.sublimetext test suite
===================================

Install sublimetext recipe with autocomplete path for eggs, some packages::
    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop =
    ...     %(test_dir)s/develop/sublimtexttest_pkg1
    ... eggs =
    ...     sublimtexttest_pkg1
    ...     zc.recipe.egg
    ...     zc.buildout
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... packages = %(test_dir)s/Products
    ... project-name = plone-recipe-sublime
    ... ignore-develop = False
    ... eggs = ${buildout:eggs}
    ... overwrite = False
    ... jedi-enabled = True
    ... sublimelinter-enabled = True
    ... sublimelinter-pylint-enabled = True
    ... sublimelinter-flake8-enabled = True
    ... """ % globals())
    >>> output_lower = system(buildout + ' -c buildout.cfg').lower()
    >>> 'installing sublimetext.' in output_lower
    True
    >>> 'tests/develop/sublimtexttest_pkg1' in output_lower
    True
    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  parts
    -  plone-recipe-sublime.sublime-project
    <BLANKLINE>
    >>> import json
    >>> ST3_settings = json.loads(read(sample_buildout, 'plone-recipe-sublime.sublime-project'))
    >>> len(ST3_settings['settings']['python_package_paths']) == 5
    True
    >>> 'SublimeLinter' in ST3_settings.keys()
    True
    >>> ST3_settings['SublimeLinter']['linters']['pylint']['@disable']
    False

SublimeText congiguration with all default options::
    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop =
    ...     %(test_dir)s/develop/sublimtexttest_pkg1
    ... eggs =
    ...     sublimtexttest_pkg1
    ...     zc.recipe.egg
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... eggs = ${buildout:eggs}
    ... """ % globals())
    >>> output = system(buildout + ' -c buildout.cfg').lower()
    >>> ST3_settings = json.loads(read(sample_buildout, 'plone-recipe-sublime.sublime-project'))
    >>> 'SublimeLinter' not in ST3_settings.keys()
    True
    >>> ST3_settings['settings']['sublimelinter']
    False
    >>> 'python_package_paths' not in ST3_settings['settings'].keys()
    True

SublimeText congiguration test with custom location, custom flake8 exacutable::

    >>> import os
    >>> import tempfile
    >>> custom_location = os.path.join(tempfile.gettempdir(), 'hshdsrthgdrts')
    >>> GLOBAL = {'custom_location': custom_location}
    >>> GLOBAL.update(globals())
    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... develop =
    ...     %(test_dir)s/develop/sublimtexttest_pkg1
    ... eggs =
    ...     sublimtexttest_pkg1
    ...     zc.recipe.egg
    ... parts = sublimetext
    ...
    ... [sublimetext]
    ... recipe = plone.recipe.sublimetext
    ... eggs = ${buildout:eggs}
    ... project-name = plone-recipe-sublime
    ... location = %(custom_location)s
    ... sublimelinter-enabled = True
    ... sublimelinter-flake8-enabled = True
    ... sublimelinter-flake8-executable = /fake/path/flake8
    ... """ % GLOBAL)
    >>> output = system(buildout + ' -c buildout.cfg').lower()
    >>> ST3_settings = json.loads(read(custom_location, 'plone-recipe-sublime.sublime-project'))
    >>> ST3_settings['SublimeLinter']['linters']['flake8']['executable'] == '/fake/path/flake8'
    True
    >>> import shutil
    >>> shutil.rmtree(custom_location)


