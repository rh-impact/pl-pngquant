from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pngquant',
    version          = '1.0.0',
    description      = 'Compress PNG images using pngquant.',
    long_description = readme,
    author           = 'brusdev',
    author_email     = 'brusdev@gmail.com',
    url              = 'http://wiki',
    packages         = ['pngquant'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'pngquant = pngquant.__main__:main'
            ]
        }
)
