"""
The Bestory Project
"""

from distutils.core import setup


def content(filename, splitlines=False):
    c = open(filename, 'r').read()
    return c.splitlines() if splitlines else c


long_description = content('README.md')
install_requires = content('requirements.txt', splitlines=True)
tests_requires = content('requirements-test.txt', splitlines=True)

setup(
    name='thebestory',
    description='The Bestory Magic-Powered Server',
    version='2016.11.0',
    url='thebestory.com',

    author='The Bestory Team',
    author_email='team@thebestory.com',

    license='',
    long_description=long_description,

    packages=['thebestory'],

    install_requires=install_requires,
    tests_require=install_requires + tests_requires,

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ),
)
