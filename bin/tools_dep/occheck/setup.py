import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(__file__)

__pkg_info__ = {}
with open(os.path.join(base_dir, 'occheck', '__pkginfo__.py')) as f:
    exec(f.read(), __pkg_info__)

setup(
    name='occheck',
    version=__pkg_info__['version'],
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime==4.7.2',
        'PyYAML==5.1'
    ],

    entry_points={
        'console_scripts': [
            'occheck = occheck.__main__:run_check'
        ]
    },
)