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
    >>> cat(sample_buildout, 'plone-recipe-sublime.sublime-project') # doctest: +SKIP
    <BLANKLINE>

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
    >>> file_contents = read(sample_buildout, 'plone-recipe-sublime.sublime-project')


