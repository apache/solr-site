Title: Install JCC
URL: pylucene/jcc/install.html
save_as: pylucene/jcc/install.html
template: lucene/pylucene/jcc/page

## Getting JCC's Source Code

JCC's source code is included with PyLucene's. If you've downloaded the PyLucene
source code already, JCC's is to be found in the _jcc_ subdirectory.

To get the JCC source code only from SVN use:<br/>
`$ svn co https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc`

## Building JCC

JCC is a Python extension written in Python and C++. It requires a Java Runtime
Environment to operate as it uses Java's reflection APIs to do its work. It is
built and installed via _distutils_ or [setuptools](https://pypi.python.org/pypi/setuptools).

- On MacOS and Windows, _setup.py_ will attempt to find a JDK on your system and
report what it found by showing the values for _JAVAHOME_ and _JAVAFRAMEWORKS_ it
was able to derive. If the JDK installation that was found is not the one you
wish to use or if you are not on MacOS or Windows, you can either edit _setup.py_
and review that the values in the _INCLUDES_, _CFLAGS_, _DEBUG_CFLAGS_, _LFLAGS_,
_JAVAC_, and _JAVADOC_ dicts are correct for your system or set **all** of the
environment variables _JCC_JDK_, _JCC_INCLUDES_, _JCC_CFLAGS_, _JCC_DEBUG_CFLAGS_,
_JCC_LFLAGS_, _JCC_JAVAC_ and _JCC_JAVADOC_, using os.pathsep as value separator
to override them. The values hereby configured are going to be compiled into JCC's
_config.py_ file and are going to be used by JCC when invoking _setuptools_ to
compile the extensions it is used to generate code for.

- At the command line, enter:
```
$ python setup.py build<br/>
$ sudo python setup.py install<br/>
```

## Requirements

JCC requires a Java Development Kit to be present. It uses the Java Native Invocation
Interface and expects _&lt;jni.h&gt;_ and the Java libraries to be present at build
and runtime.

JCC requires a C++ compiler. A recent C++ compiler for your platform is expected
to work as expected.

## Shared Mode: Support for the _--shared_ Flag

JCC includes a small runtime that keeps track of the Java VM and of Java objects
escaping it. Because there can be only one Java VM embedded in a given process
at a time, the JCC runtime must be compiled as a shared library when more than
one JCC-built Python extension is going to be imported into a given Python process.

Shared mode depends on _setuptools_' capability of building plain shared libraries
(as opposed to shared libraries for Python extensions).

Currently, shared mode is supported with _setuptools 0.6c7_ and above out of the
box on MacOS and Windows. On Linux, a patch to _setuptools_ needs to be applied
first. This patch is included in the JCC source distribution in the _jcc2/patches_
directory, _patch.43_. This patch was submitted to the _setuptools_ project via
[issue 43](https://bugs.python.org/setuptools/issue43). _setup.py_ will attempt
to apply the patch for you via monkeypatching.

The _shared mode disabled_ error reported during the build of JCC's on Linux
contains the exact instructions on how to patch the _setuptools_ installation
with _patch.43_ on your system.

Shared mode is also required when embedding Python in a Java VM as JCC's runtime
shared library is used by the JVM to load JCC and bootstrap the Python VM via the
JNI.


When shared mode is not enabled, not supported or _distutils_ is used instead
of _setuptools_, static mode is used instead. The JCC runtime code is statically
linked with each JCC-built Python extension and only one such extension can be
used in a given Python process at a time.

As setuptools grows its shared library building capability it is expected that]
more operating systems should be supported with shared mode in the future.

Shared mode can be forced off by building JCC with the _NO_SHARED_ environment'
variable set.

There are two defaults to consider here:


- Is JCC built with shared mode support or not ?

    - By default, on MacOS, Linux or Windows, this is the case when using a modern
      version of _setuptools_

    - On other operating systems shared mode support is off by default - not
      supported - because shared mode depends on _setuptools_'s capability of
      building a regular shared library which is still an experimental feature.

- Is a JCC-built Python extension built with shared mode ?<br/>By default, no,
  shared mode is enabled only with the _--shared_ command line argument.

## Notes for MacOS

On MacOS, Java is installed by Apple's setup as a framework. The values in
_setup.py_ for _INCLUDES_ and _LFLAGS_ for _darwin_ should be correct and ready
to use when _setup.py_ was able to derive _JAVAHOME_ and _JAVAFRAMEWORKS_.

  However, if you intend to use the 'system' Python from a Java VM on MacOS --
  Python embedded in Java -- you will need to add the flags _"-framework", "Python"_
  to the _LFLAGS_ value.

## Notes for Linux

JCC has been built and tested on a variety of Linux distributions, 32- and 64-bit.
Getting the java configuration correct is important and is done differently for
every distribution.<br/>For example:

- On Ubuntu, to install Java 5, these commands may be used:
```
      $ sudo apt-get install sun-java5-jdk<br/>
      $ sudo update-java-alternatives -s java-1.5.0-sun<br/>
```
The samples flags for Linux in JCC's setup.py should be close to correct.

- On Gentoo, the _java-config_ utility should be used to locate, and possibly
change, the default java installation. The sample flags for Linux in JCC's
_setup.py_ should be changed to reflect the root of the Java installation which
may be obtained via:
```
      $ java-config -O
```

See earlier section about [Shared Mode](#shared) for Linux support.

## Notes for Solaris 11 with Sun Studio C++ 12

JCC has been built and tested on Solaris 11 with Sun Studio C++ 12, Java 1.6 and
Python 2.4.

Because JCC is written in C++, Python's _distutils_ must be nudged a bit to
invoke the correct compiler. Sun Studio's C compiler is called _cc_ while its C++
compiler is called _CC_. To build JCC, use the following shell command to ensure
that the C++ compiler is used:

`$ CC=CC python setup.py build`

Shared mode is not currently implemented for Solaris, _setuptools_ needs to be
taught how to build plain shared libraries on Solaris first.

## Notes for Solaris 11.1 with GCC 4.5

JCC has been built and tested on Solaris 11.1 with gcc 4.5, Java 1.7 and Python
2.6. Make sure, you?ve already installed the following packages: gcc-4.5, jre-1.7,
jdk-1.7, python-2.6, ant, gnu-make and subversion.

Missing packages can be installed via _pkg install_.

- Edit setup.py and do the following changes: Inside JDK = { ? } change the entry
for sunos5 to: `'sunos5': '/usr/jdk/instances/jdk1.7.0',` Inside CFLAGS= {?} change
the entry for sunos5 to: `'sunos5': ['-fno-strict-aliasing', '-Wno-write-strings'],`
- `python setup.py build`
- `su python setup.py install`

## Notes for Windows

At this time, JCC has been built and tested on Win2k and WinXP with a variety of
Python and Java versions.

- Adding the Python directory to _PATH_ is recommended.
- Adding the Java directories containing the necessary DLLs and to _PATH_ is a must.
- Adding the directory containing _javac.exe_ to _PATH_ is required for shared
  mode (enabled by default if _setuptools >= 0.6c7_ is found to be installed).

## Notes for Python 2.3

To use JCC with Python 2.3, setuptools is required

- download [setuptools](https://pypi.python.org/pypi/setuptools).
- edit the downloaded _setuptools_ egg file to use python2.3 instead of python2.4.
- At the command line, run:<br/> `$ sudo sh setuptools-0.6c7-py2.4.egg`
