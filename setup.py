import os
from setuptools import setup
from steampak import VERSION


PATH_BASE = os.path.dirname(__file__)


f = open(os.path.join(PATH_BASE, 'README.rst'))
README = f.read()
f.close()

setup(
    name='steampak',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/steampak',

    description='Nicely packed tools to work with Steam APIs',
    long_description=README,
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=['steampak'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[],

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License'
    ],
)

