from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    author='AlgoÉTS',
    name='BullETS',
    description='BullETS is a Python package designed to help with the development of algorithmic trading strategies.',
    long_description=readme,
    long_description_content_type='text/markdown',
    version='0.1.1',
    license='Apache 2.0',
    python_requires='>=3.7',
    url='https://github.com/AlgoETS/BullETS',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=requirements
)
