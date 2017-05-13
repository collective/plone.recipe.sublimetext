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
    >>> run(buildout + ' -c buildout.cfg')
    Develop: '/home/nazrul/www/python/plone.recipe.sublimetext/src/plone/recipe/sublimetext/tests/develop/sublimtexttest_pkg1'
    Getting distribution for 'zc.recipe.egg>=2.0.0a3'.
    Got zc.recipe.egg 2.0.3.
    Installing sublimetext.
    <BLANKLINE>

