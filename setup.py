import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if os.path.exists('README.rst'):
    long_description = read('README.rst')
else:
    long_description = 'https://github.com/InviteBox/django-image-dimensions'

setup(
    name = "django-image-dimensions",
    version = "0.0.3",
    author = "Alexander Tereshkin",
    author_email = "atereshkin@invitebox.com",
    description = ("Automatically add dimension attributes to all <img> tags in a response to improve rendering speed on the client. "),
    license = "BSD",
    keywords = "django images performance",
    url = "https://github.com/InviteBox/django-image-dimensions",
    packages=['imagedimensions',],
    long_description=long_description,
    install_requires=('django-celery', ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",        
    ],
)
