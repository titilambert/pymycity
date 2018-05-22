from setuptools import setup, find_packages
  
REQUIRES = [
    'aiohttp',
    'bs4',
    'python-dateutil',
]

TEST_REQUIRES = [
    # doc
    'sphinx==1.6.3',
    'sphinx-rtd-theme==0.2.4',
    'sphinxcontrib-mermaid==0.2.1',
    # dev
    'pylint',
    'pycodestyle',
    'pytest',
    'pytest-cov',
    'pytest-html',
    'colorlog',
    'psutil',
]

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

long_desc = open('README.rst').read()

setup(name='pymycity',
      version='0.2.6',
      description='Get your city live information',
      long_description=long_desc,
      author='Thibault Cohen',

      author_email='titilambert@gmail.com',
      url='http://github.com/titilambert/pymycity',
      packages=PACKAGES,
      entry_points={
          'console_scripts': [
              'pymycity = pymycity.__main__:main'
          ]
      },
      install_requires=REQUIRES,
      tests_require=TEST_REQUIRES,
      classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)
