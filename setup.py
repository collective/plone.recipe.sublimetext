""""""
from setuptools import find_packages
from setuptools import setup

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = ['setuptools', 'zc.buildout', 'zc.recipe.egg']
tests_require = ['zope.testing', 'zc.buildout[test]', 'zc.recipe.egg']

entry_point = 'plone.recipe.sublimetext:Recipe'
uninstall_entry_point = 'plone.recipe.sublimetext:uninstall'
entry_points = {'zc.buildout': ['default = {0}'.format(entry_point)],
'zc.buildout.uninstall': ['default = {0}'.format(uninstall_entry_point)]}

setup(
    name='plone.recipe.sublimetext',
    version='1.0.0.dev0',
    description="SublimeText Configuration for Buildout",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 3 - Alpha",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone Zope Buildout',
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
