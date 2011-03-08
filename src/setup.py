__author__="Jiri Chadima"
__date__ ="$Mar 8, 2011 2:35:06 PM$"

from setuptools import setup,find_packages

setup (
  name = 'tweetStream',
  version = '0.2',
  packages = find_packages(),

  install_requires=['pygtk>=2'],

  author = 'Jiri Chadima',
  author_email = 'chadima.jiri@gmail.com',

  summary = 'Small python GTK app that displays one twitter feed in real-time',
  url = 'https://github.com/JirkaChadima/tweetStream',
  license = 'MIT',
  
)