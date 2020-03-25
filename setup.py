from setuptools import find_packages, setup
import io


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    separator = kwargs.get('sep', '\n')
    buf = []

    for filename in filenames:
        with io.open(filename, encoding=encoding) as file:
            buf.append(file.read())

    return separator.join(buf)

setup(
    name='terminalmenu',
    version='0.0.1',
    author='Bruno Gómez García',
    author_email='bronigege@gmail.com',
    description='Menús para la terminal.',
    long_description=read('README.md', 'CHANGELOG.rst'),
    license='MIT',
    keywords='terminal unix',
    url='https://dumasoft.io',
    packages=find_packages(),
)
