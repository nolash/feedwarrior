from setuptools import setup

setup(
    name='feedwarrior',
    version='0.4.2',
    description='feeds, warrior style',
    author='Louis Holbrook',
    author_email='dev@holbrook.no',
    packages=[
        'feedwarrior',
        'feedwarrior.cmd',
        'feedwarrior.adapters'
        ],
    install_requires=[
        'pyxdg>=0.26'
        ],
    scripts = [
        'scripts/feedwarrior',
        ]
)
