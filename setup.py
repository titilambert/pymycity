from setuptools import setup
  
install_requires = list(val.strip() for val in open('requirements.txt'))
tests_require = list(val.strip() for val in open('test_requirements.txt'))

long_desc = open('README.rst').read()

setup(name='pymycity',
      version='0.2.2',
      description='Get your city live information',
      long_description=long_desc,
      author='Thibault Cohen',

      author_email='titilambert@gmail.com',
      url='http://github.com/titilambert/pymycity',
      packages=['pymycity'],
      entry_points={
          'console_scripts': [
              'pymycity = pymycity.__main__:main'
          ]
      },
      install_requires=install_requires,
      tests_require=tests_require,
      classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)
