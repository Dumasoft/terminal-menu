from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import re
import io


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []

    for filename in filenames:
        with io.open(filename, encoding=encoding) as file:
            buf.append(file.read())

    return sep.join(buf)

version_file_name = 'terminalmenu/version.py'
version_file_contents = open(version_file_name, 'rt').read()
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = re.search(version_regex, version_file_contents, re.M)

if match:
    __version__ = match.group(1)
else:
    raise RuntimeError('No se puede encontrar la cadena de versión en %s.' % (version_file_name, ))

setup(
    name='terminal-menu',
    version=__version__,
    url='https://github.com/bronigege/terminal-menu',
    license='MIT',
    author='Bruno Gómez García',
    author_email='bronigege@gmail.com',
    description='Menús para la terminal.',
    long_description=read('README.rst', 'CHANGELOG.rst'),
    packages=find_packages(),
)
