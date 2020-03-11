from distutils.core import setup

setup(name='docker_cp',
      version='1',
      description='Copies files from your host to a container or vice versa',
      author='Elvira García',
      packages=['dockercp'],
      install_requires=['docker>=4.2.0'],
      entry_points={
          'console_scripts': ['docker-cp=dockercp:main']})