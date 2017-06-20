# _*_ coding: utf-8 _*_
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = '\n\n'.join([
    read('README.rst'),
    read('src', 'plone', 'recipe', 'sublimetext', 'README.rst'),
    read('CONTRIBUTORS.rst'),
    read('CHANGES.rst'),
])

install_requires = ['setuptools', 'zc.buildout', 'zc.recipe.egg']
tests_require = ['zope.testing', 'zc.buildout[test]', 'zc.recipe.egg']

entry_point = 'plone.recipe.sublimetext:Recipe'
uninstall_entry_point = 'plone.recipe.sublimetext:uninstall'
entry_points = {
    'zc.buildout': ['default = {0}'.format(entry_point)],
    'zc.buildout.uninstall': ['default = {0}'.format(uninstall_entry_point)]
}

setup(
    name='plone.recipe.sublimetext',
    version='1.1.1',
    description='SublimeText configuration for buildout-based Python projects',
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    keywords='python buildout plone sublime-text jedi sublimelinter buildout-recipe anaconda',
    author='Md Nazrul Islam',
    author_email='connect2nazrul@gmail.com',
    url='https://github.com/nazrulworld/plone.recipe.sublimetext',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.recipe'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={'test': tests_require},
    entry_points=entry_points,
)
