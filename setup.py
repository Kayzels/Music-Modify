"""Setup module for music modify.
    """
import os
from setuptools import setup, find_packages


def read(fname: str):
    """Read a file and save the text from that file.

    Parameters
    ----------
    fname : [str] -
        The file that should be read.

    Returns
    -------
    [str] -
        The text from the file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='music_modify',
    version='1.0.0',
    author='Kyzan Hartwig',
    author_email='kzn.hartwig1@gmail.com',
    description=("App that allows a user to modify the tags for their "
                 "music files, and download information from "
                 "different music websites."
                 ),
    license='GNU GPL v3',
    keywords="mp3 music tags",
    url="https://github.com/KyzanHartwig/Music-Modify",
    long_description=read('README.md'),
    packages=find_packages(exclude=["config"]),
    python_requires='>=3.8',
)
