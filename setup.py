from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    author='AlgoÉTS',
    name='BullETS',
    version='0.0.1',
    url='https://github.com/AlgoETS/BullETS',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=requirements
)
