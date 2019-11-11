Title: Welcome to JCC, PyLucene's code generator
URL: pylucene/jcc/index.html
save_as: pylucene/jcc/index.html
template: lucene/pylucene/jcc/page

## What is JCC ?

JCC is a C++ code generator that produces a C++ object interface wrapping a Java
library via Java's Native Interface (JNI). JCC also generates C++ wrappers that
conform to Python's C type system making the instances of Java classes directly
available to a Python interpreter.

When generating Python wrappers, JCC produces a complete Python extension module
via the distutils or [setuptools](https://pypi.python.org/pypi/setuptools) packages.

See [here](features.html) for more information and documentation about JCC.

## Requirements

JCC is supported on Mac OS X, Linux, Solaris and Windows.

JCC requires Python version 2.x (x >= 3.5) or Python version 3.x (x >= 3) and Java
version 1.x (x >= 4). Building JCC requires a C++ compiler. Use of
[setuptools](https://pypi.python.org/pypi/setuptools) is recommended.

See the [installation instructions](install.html) for more information about building
JCC from sources.

## Source Code

The source code to JCC is part of PyLucene's and can be obtained with a subversion
client from [here](https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc)

## Mailing List

If you'd like to contribute to JCC or are having issues or questions with JCC,
please subscribe to the PyLucene developer [mailing list](../mailing-lists.html)
