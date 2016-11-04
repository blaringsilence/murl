from setuptools import setup
setup(
  name = 'mrf-murl',
  packages = ['mrf_murl'], 
  version = '0.0.4',
  description = 'A URI manipulation tool aimed at web use.',
  author = 'Mariam Maarouf',
  author_email = 'mrf.mariam@gmail.com',
  url = 'https://github.com/blaringsilence/murl',
  download_url = 'https://github.com/blaringsilence/murl/tarball/0.0.4', 
  keywords = ['uri', 'web'], 
  include_package_data = True,
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)