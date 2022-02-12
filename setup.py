from setuptools import setup
import os

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()


setup(
    name='feedwarrior',
    version='0.5.2',
    description='feeds, warrior style',
    author='Louis Holbrook',
    author_email='dev@holbrook.no',
    packages=[
        'feedwarrior',
        'feedwarrior.cmd',
        'feedwarrior.adapters'
        ],
    install_requires=[
        requirements,
        ],
    scripts = [
        'scripts/feedwarrior',
        ]
)
