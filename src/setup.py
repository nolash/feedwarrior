from setuptools import setup

setup(
    name='feedwarrior',
    version='0.1.0',
    description='feeds, warrior style',
    author='Louis Holbrook',
    author_email='dev@holbrook.no',
    packages=['feedwarrior', 'feedwarrior.cmd'],
    install_requires=['xdg'],
    scripts=[
        'main.py',
        ]
)