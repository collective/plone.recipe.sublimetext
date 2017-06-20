.. image:: https://img.shields.io/pypi/status/plone.recipe.sublimetext.svg
    :target: https://pypi.python.org/pypi/plone.recipe.sublimetext/
    :alt: Egg Status

.. image:: https://img.shields.io/travis/nazrulworld/plone.recipe.sublimetext/master.svg
    :target: http://travis-ci.org/nazrulworld/plone.recipe.sublimetext
    :alt: Travis Build Status

.. image:: https://img.shields.io/coveralls/nazrulworld/plone.recipe.sublimetext/master.svg
    :target: https://coveralls.io/r/nazrulworld/plone.recipe.sublimetext
    :alt: Test Coverage

.. image:: https://img.shields.io/pypi/pyversions/plone.recipe.sublimetext.svg
    :target: https://pypi.python.org/pypi/plone.recipe.sublimetext/
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/plone.recipe.sublimetext.svg
    :target: https://pypi.python.org/pypi/plone.recipe.sublimetext/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/plone.recipe.sublimetext.svg
    :target: https://pypi.python.org/pypi/plone.recipe.sublimetext/
    :alt: License


.. contents::

Introduction
============

``plone.recipe.sublimetext`` is the buildout recipe for `ST3`_ lover who wants python IDE like features while developing python `Buildout`_ based project. This tool will help them to create per project basis sublimetext settings with appropriate paths location assignment. Currently ``plone.recipe.sublimetext`` comes with supporting settings for `Anaconda`_ (the all-in-one package), `Jedi`_, `Sublimelinter`_, `Sublimelinter-Flake8`_, `Sublimelinter-Pylint`_.
A general question may arise that why we will use this tool, whether we can create `ST3`_ project settings easily (we have better knowledge over `ST3`_ configuration)?
Well i completely agree with you, but if you want to get benefited from `Anaconda`_ or `Jedi`_'s python autocompletion feature (basically I am lover of autocompletion), you have to add all eggs links for `Anaconda`_ or `Jedi`_'s paths settings and it is hard to manage eggs links manually if the size of project is big (think about any `Plone`_ powered project), beside `Sublimelinter-Pylint`_ also need list of paths to be added to sys.path  to find modules.

Installation
============

Install ``plone.recipe.sublimetext`` is simple enough, just need to create a section for ``sublimetext`` to your buildout. Before using ``plone.recipe.sublimetext`` make sure  `Jedi`_, `Sublimelinter`_, `Sublimelinter-Flake8`_ and/or `Sublimelinter-Pylint`_ plugins are already installed at your `ST3`_. You could follow full [`instruction here
<https://nazrulworld.wordpress.com/2017/05/06/make-sublime-text-as-the-best-ide-for-full-stack-python-development>`_] if not your `ST3`_ setup yet. Flake8 linter need `flake8 executable <https://pypi.python.org/pypi/flake8>`_ available globally (unless you are going to use local flake8), also it is recommended you install some awsome flake8 plugins (flake8-isort, flake8-coding, pep8-naming, flake8-blind-except, flake8-quotes and more could find in pypi)

    Example Buildout::

        [buildout]
        parts += sublimetext

        [sublimetext]
        recipe = plone.recipe.sublimetext
        eggs = ${buildout:eggs}
        jedi-enabled = True
        sublimelinter-enabled = True
        sublimelinter-pylint-enabled = True

Available Options
-----------------

eggs
    Required: Yes

    Default: None

    Your project's list of eggs, those are going to be added in path location for `Jedi`_ and/or `Sublimelinter-Pylint`_ or `Anaconda`_.

overwrite
    Required: No

    Default: False

    This option indicates whether existing settings should be cleaned first or just updating changes.
    This situation may happen, you did create settings file manually with other configuration (those are not managed by ``plone.recipe.sublimetext``) and you want keep those settings intact.

python-executable
    Required: No

    Default: ``plone.recipe.sublimetext`` will find current python executable path.

    The python executable path for current project, if you are using virtual environment then should be that python path. FYI: ${home} and ${project} variable should work.

project-name
    Required: No

    Default: if you have a existing `ST3`_ project file(settings file) in project/buildout's root directory, ``plone.recipe.sublimetext`` will choose it as ``project-name``, other than project/buildout directory name will become as ``project-name``

    Don't add suffix ``.sublime-project``, when you provide the project name.

jedi-enabled
    Required: No

    Default: False

    This option is related to enable/disable Sublime `Jedi`_

sublimelinter-enabled
    Required: No

    Default: False

    Whether `Sublimelinter`_'s features you want to use or not.

sublimelinter-pylint-enabled
    Required: No

    Default: False

     If you want to use `Sublimelinter-Pylint`_ or not; ``sublimelinter-enabled`` option will be respected, means if parent option is set as disabled but you enable this option will not work.

sublimelinter-flake8-enabled
    Required: No

    Default: False

    Whether you want to use `Sublimelinter-Flake8`_ or not. Like ``sublimelinter-pylint-enabled`` parent option will be respected.

sublimelinter-flake8-executable
    Required: No

    Default: False

    Project specific `Flake8`_ executable path, this will give you lots flexibility over using global `Flake8`_ executable, because each project might have separate `Python`_ version.

anaconda-enabled
    Required: No

    Default: False

    This option is related to whether you want to enable `Anaconda`_ the all-in-one python IDE package!

anaconda-linting-enabled
    Required: No

    Default: True

    If want to other library for liniting (i.e sublimelinter), keep it disabled, other than should be enabled. Like other parent options, it will respect parent (``anaconda-enabled``) option.

anaconda-completion-enabled
    Required: No

    Default: True

    Anaconda is using `Jedi`_ engine for autocompletion, but if you want to use Sublime-Jedi other than provided by Anaconda, make it disabled.

anaconda-pylint-enabled
    Required: No

    Default: False

    By default `Anaconda`_ liniting doing validation using PyFlakes, PEP8, PEP257. But you can use Pylint instead of PyFlakes by enabling this option.

anaconda-validate-imports
    Required: No

    Default: True

    It is always good that you want to see any invalid imports (for example: ``from fake.foo import bar``), but if you don't want this just disabled this option.

anaconda-pep8-ignores
    Required: No

    Default: ''

    If you want ignore some pep8 checklist (i.e N802 is for pep8 naming).

ignore-develop
    Required: No

    Default: False

    If you don't want development eggs, should go for autocompletion.

ignores
    Required: No

    Default: ""

    If you want specific eggs should not go for autocompletion.

packages
    Required: No

    Default: ""

    Location of some python scripts or non standard modules (don't have setup file), you want to be in system path.

Links
=====

Code repository:

    https://github.com/nazrulworld/plone.recipe.sublimetext

Continuous Integration:

    https://travis-ci.org/nazrulworld/plone.recipe.sublimetext

Issue Tracker:

    https://github.com/nazrulworld/plone.recipe.sublimetext/issues


Known Issues
============

- `Sublimelinter-Flake8`_ might stop working if `flake8-plone-api <https://pypi.python.org/pypi/flake8-plone-api>`_ is installed as until 1.2 version, `flake8-plone-api` don't support SublimeText (linting), see pull request `here <https://github.com/gforcada/flake8-plone-api/pull/18>`_ . That means upcoming version will support hopefully. It could happen, either you are using global or virtualenv flake8. You can see error in `ST3`_ console::

    flake8_plone_api-1.2-py2.7.egg/flake8_plone_api.py", line 16, in run
    with open(self.filename) as f:
    IOError: [Errno 2] No such file or directory: 'stdin'


.. _`ST3`: https://www.sublimetext.com/3
.. _`Buildout`: http://www.buildout.org/en/latest/
.. _`Jedi`: https://github.com/srusskih/SublimeJEDI
.. _`Sublimelinter`: http://sublimelinter.readthedocs.io/en/latest/
.. _`Sublimelinter-Flake8`: https://github.com/SublimeLinter/SublimeLinter-flake8
.. _`Sublimelinter-Pylint`: https://github.com/SublimeLinter/SublimeLinter-pylint
.. _`Plone`: https://plone.org/
.. _`Flake8`: https://pypi.python.org/pypi/flake8
.. _`Python`: https://www.python.org/
.. _`Anaconda`: https://nazrul.me/2017/06/10/make-anaconda-powered-sublimetext-as-powerful-python-ide-for-full-stack-development/
