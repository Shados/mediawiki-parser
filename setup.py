#!/bin/env python

import os
from setuptools import setup
from distutils.cmd import Command
from distutils.command.build import build as _build

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def inputNewer(inputFile, outputFile):
    if not os.path.exists(outputFile):
        return True
    elif os.stat(inputFile).st_mtime - os.stat(outputFile).st_mtime > 1:
        return True
    else:
        return False

def makeparsers():
    from pijnu import makeParser
    import os
    inputFile = "preprocessor.pijnu"
    outputFile = os.path.join("mediawiki_parser", "preprocessorParser.py")
    if inputNewer(inputFile, outputFile):
        preprocessorGrammar = file(inputFile).read()
        makeParser(preprocessorGrammar, outputPath="mediawiki_parser")

    inputFile = "mediawiki.pijnu"
    outputFile = os.path.join("mediawiki_parser", "wikitextParser.py")
    if inputNewer(inputFile, outputFile):
        mediawikiGrammar = file(inputFile).read()
        makeParser(mediawikiGrammar, outputPath="mediawiki_parser")

class build_parsers(Command):
    description = "Build the pijnu parsers for mediawiki_parser"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            makeparsers()

class build(_build):
    sub_commands = [ ('build_parsers', None) ] + _build.sub_commands 


setup(
    name="mediawiki-parser",
    author="erikrose",
    version="0.3.00",
    description=("",),
    long_description=read('README.rst'),
    packages=[
        "mediawiki_parser"
        ],
    scripts=[],
    data_files=[],
    install_requires=[ ],
    cmdclass={'build_parsers': build_parsers, 'build': build}
)
