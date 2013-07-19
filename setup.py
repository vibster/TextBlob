import sys
import os

import text
from distutils.util import convert_path

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

    def _find_packages(where='.', exclude=()):
        """Return a list all Python packages found within directory 'where'

        'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
        will be converted to the appropriate local path syntax.  'exclude' is a
        sequence of package names to exclude; '*' can be used as a wildcard in the
        names, such that 'foo.*' will exclude all subpackages of 'foo' (but not
        'foo' itself).
        """
        out = []
        stack = [(convert_path(where), '')]
        while stack:
            where, prefix = stack.pop(0)
            for name in os.listdir(where):
                fn = os.path.join(where, name)
                if ('.' not in name and os.path.isdir(fn) and
                        os.path.isfile(os.path.join(fn, '__init__.py'))):
                    out.append(prefix+name)
                    stack.append((fn, prefix + name + '.'))
        for pat in list(exclude)+['ez_setup', 'distribute_setup']:
            from fnmatch import fnmatchcase
            out = [item for item in out if not fnmatchcase(item, pat)]
        return out

    find_packages = _find_packages


PUBLISH = "python setup.py register sdist upload"
TEST = 'tox'

if sys.argv[-1] == 'publish':
    os.system(PUBLISH)
    sys.exit()

if sys.argv[-1] == 'test':
    try:
        __import__('tox')
    except ImportError:
        print('tox required.')
        sys.exit(1)

    os.system(TEST)
    sys.exit()


def cheeseshopify(rst):
    '''Since PyPI doesn't support the `code-block` or directive, this replaces
    all `code-block` directives with `::`.
    '''
    ret = rst.replace(".. code-block:: python", "::").replace(":code:", "")
    return ret

with open('README.rst') as fp:
    long_desc = cheeseshopify(fp.read())

setup(
    name='textblob',
    version=text.__version__,
    description='Simple, Pythonic text processing. Sentiment analysis, '
                'POS tagging, noun phrase parsing, and more.',
    long_description=long_desc,
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/TextBlob',
    install_requires=['PyYAML'],
    packages=find_packages(),
    package_data={
        "text": ["*.txt", "*.xml"],
    },
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ),
    tests_require=['nose'],
)
