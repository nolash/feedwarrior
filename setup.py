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

f = open('README.md', 'r')
description = f.read()
f.close()

setup(
    packages=[
        'feedwarrior',
        'feedwarrior.cmd',
        'feedwarrior.adapters',
        'feedwarrior.runnable',
        ],
    install_requires=[
        requirements,
        ],
    entry_points = {
        'console_scripts': [
            'feedwarrior = feedwarrior.runnable.main:main',
            ],
        },
    data_files=[("man/man1", ["man/man1/feedwarrior.1"],)],
    long_description=description,
    long_description_content_type='text/markdown',
)
