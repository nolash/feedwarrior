from setuptools import setup

setup(
    name='feedwarrior',
    version='0.5.0',
    description='feeds, warrior style',
    author='Louis Holbrook',
    author_email='dev@holbrook.no',
    packages=[
        'feedwarrior',
        'feedwarrior.cmd',
        'feedwarrior.adapters'
        ],
    install_requires=[
        'pyxdg>=0.26',
        'tasklib>=1.3.0,<2.0.0',
        ],
    scripts = [
        'scripts/feedwarrior',
        ]
)
