from os.path import dirname, join
from setuptools import setup


version = '0.1.0'


def read(fname):
    return open(join(dirname(__file__), fname)).read()


with open("requirements.txt", "r") as f:
    install_reqs = f.readlines()

setup(name='noaa_tools',
      version=version,
      author="Chad Dotson",
      author_email="chad@cdotson.com",
      description="Utilities for fetching/processing data from NOAA, including tools for downloading and overlaying "
                  "radar images from the Ridge radar sites.",
      license="GNUv3",
      keywords=["noaa", "radar", "tools", "weather"],
      url="https://github.com/chaddotson/noaa_tools",
      download_url = 'https://github.com/chaddotson/noaa_tools/tarball/0.1.0',
      packages=['noaa_tools'],
      long_description=read("README.rst"),
      install_requires=install_reqs,
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'fetch_radar_image_cli = scripts.fetch_radar_image_cli:main',
          ]
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      ]

)


    # test_suite='nose.collector',
    # tests_require=['nose'],
