Changelog
=========

1.2.1 (unreleased)
------------------

- Nothing changed yet.


1.2.0 (2018-03-05)
------------------

New features:

- (breaking) Sublime​Linter 4.x version support is added, that means older than version 4 might not working (although not tested.). If you face any problem, we suggest either you will update Sublime​Linter version or use older version of `plone.recipe.sublimetext` (1.1.6)
- pylint executable path now can be provided.


1.1.6 (2018-01-24)
------------------

- Set a default folder_exclude_patterns for performance, and also to eliminate noise when looking up packages.
- Set follow_symlinks to true.
- split out omelette in own project folder setting, for being able to exclude 'parts'.
  [sunew]


1.1.5 (2017-10-31)
------------------

- Flake8 executable path: Enable to use `buildout relative`/`user's home relative` path. Means now it is possible to use buildout, sublimetext style relative path.
  [nazrulworld]


1.1.4 (2017-08-11)
------------------

- Enable using the omelette as a basis for jedi.
  [sunew]


1.1.3 (2017-07-30)
------------------

- Repository ownership transfered to `Plone Collective <https://collective.github.io/>`_


1.1.2 (2017-07-02)
------------------

Bugfixes:

- [#8] `Install using pip in virtualenv got error <https://github.com/collective/plone.recipe.sublimetext/issues/8>`_


1.1.1 (2017-06-20)
------------------

Bugfixes:

- [#7]`python_interpreter` value as list but expected as string.
  [nazrulworld]


1.1.0 (2017-06-07)
------------------

New features:

- [#4] `Anaconda support <https://github.com/collective/plone.recipe.sublimetext/issues/4>`_ [nazrulworld]


1.0.1 (2017-05-16)
------------------

Bugfixes:

- [#1] `Required options for sublime text project file is missing <https://github.com/collective/plone.recipe.sublimetext/issues/1>`_


1.0.0 (2017-05-15)
------------------

- Initial release.
  [nazrulworld]
