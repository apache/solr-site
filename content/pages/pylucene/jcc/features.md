Title: Features
URL: pylucene/jcc/features.html
save_as: pylucene/jcc/features.html
template: lucene/pylucene/jcc/page
slug: pylucene-jcc-features

## Warning
*Before calling any PyLucene API that requires the Java VM, start it by calling
_initVM(classpath, ...)_. More about this function in [here](#api).*

## Installing JCC

JCC is a Python extension written in Python and C++. It requires a Java Runtime
Environment (JRE) to operate as it uses Java's reflection APIs to do its work.
It is built and installed via _distutils_ or _setuptools_.

See [installation](install.html) for more information and operating system
specific notes.

## Invoking JCC

JCC is installed as a package and how to invoke it depends on the Python version
used:

- python 3.6: **python -m jcc**
- python 2.7: **python -m jcc**
- python 2.6: **python -m jcc.\_\_main\_\_**
- python 2.5: **python -m jcc**
- python 2.4:
    - no setuptools: **python _site-packages_/jcc/\_\_init\_\_.py**
    - with setuptools: **python _site-packages_/_jcc egg directory_/jcc/\_\_init\_\_.py**
- python 2.3: **python _site-packages_/_jcc egg directory_/jcc/\_\_init\_\_.py**

## Generating C++ and Python wrappers with JCC

JCC started as a C++ code generator for hiding the gory details of accessing
methods and fields on Java classes via Java's
[Native Invocation Interface](https://java.sun.com/j2se/1.5.0/docs/guide/jni/spec/invocation.html).
These C++ wrappers make it possible to access a Java object as if it was a regular
C++ object.

It then became apparent that JCC could also generate the C++ wrappers for making
these classes available to Python. Every class that gets thus wrapped becomes a
[CPython type](https://docs.python.org/2/extending/newtypes.html).

JCC generates wrappers for all public classes that are requested by name on the
command line or via the _--jar_ command line argument. It generates wrapper methods
for all public methods and fields on these classes whose return type and parameter
types are found in one of the following ways:

- the type is one of the requested classes
- the type is one of the requested classes' superclass or implemented interfaces
- the type is available from one of the packages listed via the _--package_ command
  line argument

Overloaded methods are supported and are selected at runtime on the basis of the
type and number of arguments passed in.

JCC does not generate wrappers for methods or fields which don't satisfy these
requirements. Thus, JCC can avoid generating code for runaway transitive closures
of type dependencies.

JCC generates property accessors for a property called _field_ when it finds Java
methods named _setField(value)_, _getField()_ or _isField()_.

The C++ wrappers are declared in a C++ namespace structure that mirrors the Java
classes' Java packages. The Python types are declared in a flat namespace at the
top level of the resulting Python extension module.

JCC's command-line arguments are best illustrated via the PyLucene example:

```
$ python -m jcc           # run JCC to wrap
    --jar lucene.jar      # all public classes in the lucene jar file
    --jar analyzers.jar   # and the lucene analyzers contrib package
    --jar snowball.jar    # and the snowball contrib package
    --jar highlighter.jar # and the highlighter contrib package
    --jar regex.jar       # and the regex search contrib package
    --jar queries.jar     # and the queries contrib package
    --jar extensions.jar  # and the Python extensions package
    --package java.lang   # including all dependencies found in the
                          # java.lang package
    --package java.util   # and the java.util package
    --package java.io     # and the java.io package
      java.lang.System    # and to explicitely wrap java.lang.System
      java.lang.Runtime   # as well as java.lang.Runtime
      java.lang.Boolean   # and java.lang.Boolean
      java.lang.Byte      # and java.lang.Byte
      java.lang.Character # and java.lang.Character
      java.lang.Integer   # and java.lang.Integer
      java.lang.Short     # and java.lang.Short
      java.lang.Long      # and java.lang.Long
      java.lang.Double    # and java.lang.Double
      java.lang.Float     # and java.lang.Float
      java.text.SimpleDateFormat
                          # and java.text.SimpleDateFormat
      java.io.StringReader
                          # and java.io.StringReader
      java.io.InputStreamReader
                          # and java.io.InputStreamReader
      java.io.FileInputStream
                          # and java.io.FileInputStream
      java.util.Arrays    # and java.util.Arrays
    --exclude org.apache.lucene.queryParser.Token
                          # while explicitely not wrapping
                          # org.apache.lucene.queryParser.Token
    --exclude org.apache.lucene.queryParser.TokenMgrError
                          # nor org.apache.lucene.queryParser.TokenMgrError
    --exclude org.apache.lucene.queryParser.ParseException
                          # nor.apache.lucene.queryParser.ParseException
    --python lucene       # generating Python wrappers into a module
                          # called lucene
    --version 2.4.0       # giving the Python extension egg version 2.4.0
    --mapping org.apache.lucene.document.Document
              'get:(Ljava/lang/String;)Ljava/lang/String;'
                          # asking for a Python mapping protocol wrapper
                          # for get access on the Document class by
                          # calling its get method
    --mapping java.util.Properties
              'getProperty:(Ljava/lang/String;)Ljava/lang/String;'
                          # asking for a Python mapping protocol wrapper
                          # for get access on the Properties class by
                          # calling its getProperty method
    --sequence org.apache.lucene.search.Hits
               'length:()I'
               'doc:(I)Lorg/apache/lucene/document/Document;'
                          # asking for a Python sequence protocol wrapper
                          # for length and get access on the Hits class by
                          # calling its length and doc methods
    --files 2             # generating all C++ classes into about 2 .cpp
                          # files
    --build               # and finally compiling the generated C++ code
                          # into a Python egg via setuptools - when
                          # installed - or a regular Python extension via
                          # distutils or setuptools otherwise
    --module collections.py
                          # copying the collections.py module into the egg
    --install             # installing it into Python's site-packages
                          # directory.
```

There are limits to both how many files can fit on the command line and how large
a C++ file the C++ compiler can handle. By default, JCC generates one large C++
file containing the source code for all wrapper classes.

Using the _--files_ command line argument, this behaviour can be tuned to
workaround various limits:<br/> for example:

- to break up the large wrapper class file into about 2 files:<br/>`--files 2`
- to break up the large wrapper class file into about 10 files:<br/>`--files 10`
- to generate one C++ file per Java class wrapped:<br/>`--files separate`

The _--prefix_ and _--root_ arguments are passed through to _distutils_' _setup()_.

## Classpath considerations

When generating wrappers for Python, the JAR files passed to JCC via _--jar_ are
copied into the resulting Python extension egg as resources and added to the extension
module's _CLASSPATH_ variable. Classes or JAR files that are required by the classes
contained in the argument JAR files need to be made findable via JCC's _--classpath_
command line argument. At runtime, these need to be appended to the extension's
_CLASSPATH_ variable before starting the VM with _initVM(CLASSPATH)_.

To have such required jar files also automatically copied into resulting Python
extension egg and added to the classpath at build and runtime, use the _--include_
option. This option works like the _--jar_ option except that no wrappers are
generated for the classes contained in them unless they're explicitly named on
the command line.

When more than one JCC-built extension module is going to be used in the same
Python VM and these extension modules share Java classes, only one extension module
should be generated with wrappers for these shared classes. The other extension
modules must be built by importing the one with the shared classes by using the
_--import_ command line parameter. This ensures that only one copy of the
wrappers for the shared classes are generated and that they are compatible among
all extension modules sharing them.

## Using _distutils_ vs _setuptools_

By default, when building a Python extension, if _setuptools_ is found to be
installed, it is used over _distutils_. If you want to force the use of _distutils_
over _setuptools_, use the _--use-distutils_ command line argument.

## Distributing an egg

The _--bdist_ option can be used to ask JCC to invoke _distutils_ with _bdist_
or _setuptools_ with _bdist_egg_. If _setuptools_ is used, the resulting egg has
to be installed with the [_easy_install_](https://setuptools.readthedocs.io/en/latest/easy_install.html)
installer which is normally part of a Python installation that includes _setuptools_.

## JCC's runtime API functions

JCC includes a small runtime component that is compiled into any Python extension
it produces.

This runtime component makes it possible to manage the Java VM from Python. Because
a Java VM can be configured with a myriad of options, it is not automatically started
when the resulting Python extension module is loaded into the Python interpreter.

Instead, the _initVM()_ function must be called from the main thread before using
any of the wrapped classes. It takes the following keyword arguments:

-
_classpath_<br/>
A string containing one or more directories or jar files for the Java VM to search
for classes. Every Python extension produced by JCC exports a _CLASSPATH_ variable
that is hardcoded to the jar files that it was produced from. A copy of each jar file
is installed as a resource file with the extension when JCC is invoked with the
_--install_ command line argument. This parameter is optional and defaults to the
_CLASSPATH_ string exported by the module
_initVM_ is imported from.
```
    >>> import lucene
    >>> lucene.initVM(classpath=lucene.CLASSPATH)
```

-
_initialheap_<br/>
The initial amount of Java heap to start the Java VM with. This argument is a string
that follows the same syntax as the similar _-Xms_ java command line argument.
```
    >>> import lucene
    >>> lucene.initVM(initialheap='32m')
    >>> lucene.Runtime.getRuntime().totalMemory()
    33357824L
```

-
_maxheap_<br/>
The maximum amount of Java heap that could become available to the Java VM. This
argument is a string that follows the same syntax as the similar _-Xmx_ java command
line argument.

-
_maxstack_<br/>
The maximum amount of stack space that available to the Java VM. This argument
is a string that follows the same syntax as the similar _-Xss_ java command line
argument.

-
_vmargs_<br/>
A string of comma separated additional options to pass to the VM startup rountine.
These are passed through as-is. For example:
```
    >>> import lucene
    >>> lucene.initVM(vmargs='-Xcheck:jni,-verbose:jni,-verbose:gc')
```

The _initVM()_ and _getVMEnv()_ functions return a JCCEnv object that has a few
utility methods on it:

-
_attachCurrentThread(name, asDaemon)_<br/>Before a thread created in Python or
elsewhere but not in the Java VM can be used with the Java VM, this method needs
to be invoked. The two arguments it takes are optional and self-explanatory.

-
_detachCurrentThread()_
The opposite of _attachCurrentThread()_. This method should be used with extreme
caution as Python's and java VM's garbage collectors may use a thread detached
too early causing a system crash. The utility of this method seems dubious at the
moment.

There are several differences between JNI's _findClass()_ and Java's _Class.forName()_:

-
className is a '/' separated string of names

-
the class loaders are different, _findClass()_ may find classes that _Class.forName()_ won't.

For example:

```
    >>> from lucene import *
    >>> initVM(CLASSPATH)
    >>> findClass('org/apache/lucene/document/Document')
    &lt;Class: class org.apache.lucene.document.Document&gt;
    >>> Class.forName('org.apache.lucene.document.Document')
    Traceback (most recent call last):
    File "&lt;stdin&gt;", line 1, in &lt;module&gt;
    lucene.JavaError: java.lang.ClassNotFoundException: org/apache/lucene/document/Document
    &gt&gt&gt Class.forName('java.lang.Object')
    &lt;Class: class java.lang.Object&gt;
```

## Type casting and instance checks

Many Java APIs are declared to return types that are less specific than the types
actually returned. In Java 1.5, this is worked around with type parameters. JCC
generates code to heed type parameters unless the _--no-generics_ is used. See
next section for details on Java generics support.

In C++, casting the object into its actual type is supported via the regular C
casting operator.

In Python each wrapped class has a class method called _cast__ that implements
the same functionality.

Similarly, each wrapped class has a class method called _instance__ that tests
whether the wrapped java instance is of the given type. For example:

```
    if BooleanQuery.instance_(query):
        booleanQuery = BooleanQuery.cast_(query)

    print booleanQuery.getClauses()
```

## Handling generic classes

Java 1.5 added support for parameterized types. JCC generates code to heed type
parameters unless the _--no-generics_ command line parameter is used. Java type
parameterization is a runtime feature. The same class is used for all its
parameterizations. Similarly, JCC wrapper objects all use the same class but store
type parameterizations on instances and make them accessible as a tuple via the
_parameters__ property.


For example, an _ArrayList&lt;Document&gt;_ instance, has _(&lt;type 'Document'&gt;,)_
for _parameters__ and its _get()_ method uses that type parameter to wrap its return
values.

To allocate an instance of a generic Java class with specific type parameters use
the _of_()_ method. This method accepts one or more Python wrapper classes to use
as type parameters. For example, _java.util.ArrayList&lt;E&gt;_ is declared to
accept one type parameter. Its wrapper's _of_()_ method hence accepts one parameter,
a Python class, to use as type parameter for the return type of its _get()_ method,
among others:

```
    &gt&gt&gt a = ArrayList().of_(Document)
    &gt&gt&gt a
    &lt;ArrayList: []&gt;
    &gt&gt&gt a.parameters_
    (&lt;type 'Document'&gt;,)
    >>> a.add(Document())
    True
    >>> a.get(0)
    &lt;Document: Document&lt;&gt;&gt;
```

The use of type parameters is, of course, optional. A generic Java class can still
be used as before, without type parameters. Downcasting from _Object_ is then necessary:

```
    >>> a = ArrayList()
    >>> a
    &lt;ArrayList: []&gt;
    >>> a.parameters_
    (None,)
    >>> a.add(Document())
    True
    >>> a.get(0)
    &lt;Object: Document&lt;&gt;&gt;
    >>> Document.cast_(a.get(0))
    &lt;Document: Document&lt;&gt;&gt;
```

## Handling arrays

Java arrays are wrapped with a C++ JArray template. The _[]_ is available for read
access. This template, _JArray&lt;T&gt;_, accomodates all java primitive types,
_jstring_, _jobject_ and wrapper class arrays.

Java arrays are returned to Python in a _JArray_ wrapper instance that implements
the Python sequence protocol. It is possible to change an array's elements but
not to change an array's size.

To convert a char array to a Python string use a _''.join(array)_ construct.

Any Java method expecting an array can be called with the corresponding sequence
object from python.

To instantiate a Java array from Python, use one of the following forms:

```
    >>> array = JArray('int')(size)
    # the resulting Java int array is initialized with zeroes

    >>> array = JArray('int')(sequence)
    # the sequence must only contain ints
    # the resulting Java int array contains the ints in the sequence
```

Instead of _'int'_, you may also use one of _'object'_, _'string'_, _'bool'_,
_'byte'_, _'char'_, _'double'_, _'float'_, _'long'_ and _'short'_ to create an
array of the corresponding type.

Because there is only one wrapper class for object arrays, the _JArray('object')_
type's constructor takes a second argument denoting the class of the object elements.
This argument is optional and defaults to _Object_.

As with the _Object_ types, the _JArray_ types also include a _cast__ method. This
method becomes useful when the array returned to Python is wrapped as a plain _Object_.
This is the case, for example, with nested arrays since there is no distinct Python
type for every different java object array class - all java object arrays are wrapped
by _JArray('object')_. For example:

```
# cast obj to an array of ints
>>> JArray('int').cast_(obj)
# cast obj to an array of Document
>>> JArray('object').cast_(obj, Document)
```

In both cases, the java type of obj must be compatible with the array type it is
being cast to.

```
    # using nested array:

    >>> d = JArray('object')(1, Document)
    >>> d[0] = Document()
    >>> d
    JArray&lt;object&gt;[&lt;Document: Document&lt;>>]
    >>> d[0]
    &lt;Document: Document&lt;&gt;&gt;
    >>> a = JArray('object')(2)
    >>> a[0] = d
    >>> a[1] = JArray('int')([0, 1, 2])
    >>> a
    JArray&lt;object&gt;[&lt;Object: [Lorg.apache.lucene.document.Document;@694f12&gt;, &lt;Object: [I@234265&gt;]
    >>> a[0]
    &lt;Object: [Lorg.apache.lucene.document.Document;@694f12&gt;
    >>> a[1]
    &lt;Object: [I@234265&gt;
    >>> JArray('object').cast_(a[0])[0]
    &lt;Object: Document&lt;&gt;&gt;
    >>> JArray('object').cast_(a[0], Document)[0]
    &lt;Document: Document&lt;&gt;&gt;
    >>> JArray('int').cast_(a[1])
    JArray&lt;int&gt;[0, 1, 2]
    >>> JArray('int').cast_(a[1])[0]
    0
```

To verify that a Java object is of a given array type, use the _instance_()_ method
available on the array type. This is not the same as verifying that it is assignable
with elements of a given type. For example, using the arrays created above:

```
    # is d array of Object ? are d's elements of type Object ?
    >>> JArray('object').instance_(d)
    True

    # can it receive Object instances ?
    >>> JArray('object').assignable_(d)
    False

    # is it array of Document ? are d's elements of type Document ?
    >>> JArray('object').instance_(d, Document)
    True

    # is it array of Class ? are d's elements of type Class ?
    >>> JArray('object').instance_(d, Class)
    False

    # can it receive Document instances ?
    >>> JArray('object').assignable_(d, Document)
    True
```

## Exception reporting

Exceptions that occur in the Java VM and that escape to C++ are reported as a
_javaError_ C++ exception. When using Python wrappers, the C++ exceptions are handled
and reported with Python exceptions. When using C++ only, failure to handle the
exception in your C++ code will cause the process to crash.

Exceptions that occur in the Java VM and that escape to the Python VM are reported
with a _JavaError_ python exception object. The _getJavaException()_ method can
be called on _JavaError_ objects to obtain the original java exception object
wrapped as any other Java object. This Java object can be used to obtain a Java
stack trace for the error, for example.

Exceptions that occur in the Python VM and that escape to the Java VM, as for
example can happen in Python extensions (see topic below) are reported to the
Java VM as a _RuntimeException_ or as a _PythonException_ when using shared mode.
See [installation instructions](install.html) for more information about shared mode.

## Writing Java class extensions in Python

JCC makes it relatively easy to extend a Java class from Python. This is done
via an intermediary class written in Java that implements a special method called
_pythonExtension()_ and that declares a number of native methods that are to be
implemented by the actual Python extension.

When JCC sees these special extension java classes it generates the C++ code
implementing the native methods they declare. These native methods call the
corresponding Python method implementations passing in parameters and returning
the result to the Java VM caller.

For example, to implement a Lucene analyzer in Python, one would implement first
such an extension class in Java:

```
package org.apache.pylucene.analysis;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import java.io.Reader;

public class PythonAnalyzer extends Analyzer {
    private long pythonObject;

    public PythonAnalyzer()
    {
    }

    public void pythonExtension(long pythonObject)
    {
        this.pythonObject = pythonObject;
    }
    public long pythonExtension()
    {
        return this.pythonObject;
    }

    public void finalize()
        throws Throwable
    {
        pythonDecRef();
    }

    public native void pythonDecRef();
    public native TokenStream tokenStream(String fieldName, Reader reader);
}
```

The _pythonExtension()_ methods is what makes this class recognized as an extension
class by JCC. They should be included verbatim as above along with the declaration of
the _pythonObject_ instance variable.

The implementation of the native _pythonDecRef()_ method is generated by JCC and
is necessary because it seems that _finalize()_ cannot itself be native. Since an
extension class wraps the Python instance object it's going to be calling methods
on, its ref count needs to be decremented when this Java wrapper class disappears.
A declaration for _pythonDecRef()_ and a _finalize()_ implementation should always
be included verbatim as above.

Really, the only non boilerplate user input is the constructor of the class and
the other native methods, _tokenStream()_ in the example above.

The corresponding Python class(es) are implemented as follows:

```
class _analyzer(PythonAnalyzer):
  def tokenStream(_self, fieldName, reader):
      class _tokenStream(PythonTokenStream):
          def __init__(self_):
              super(_tokenStream, self_).__init__()
              self_.TOKENS = ["1", "2", "3", "4", "5"]
              self_.INCREMENTS = [1, 2, 1, 0, 1]
              self_.i = 0
              self_.posIncrAtt = self_.addAttribute(PositionIncrementAttribute.class_)
              self_.termAtt = self_.addAttribute(TermAttribute.class_)
              self_.offsetAtt = self_.addAttribute(OffsetAttribute.class_)
          def incrementToken(self_):
              if self_.i == len(self_.TOKENS):
                  return False
              self_.termAtt.setTermBuffer(self_.TOKENS[self_.i])
              self_.offsetAtt.setOffset(self_.i, self_.i)
              self_.posIncrAtt.setPositionIncrement(self_.INCREMENTS[self_.i])
              self_.i += 1
              return True
          def end(self_):
              pass
          def reset(self_):
              pass
          def close(self_):
              pass
      return _tokenStream()
```

When an _\_\_init\_\_()_ is declared, _super()_ must be called or else the Java
wrapper class will not know about the Python instance it needs to invoke.

When a java extension class declares native methods for which there are public
or protected equivalents available on the parent class, JCC generates code that
makes it possible to call _super()_ on these methods from Python as well.

There are a number of extension examples available in PyLucene's test
[suite](https://svn.apache.org/viewvc/lucene/pylucene/trunk/test3) and
[samples](https://svn.apache.org/viewvc/lucene/pylucene/trunk/samples).

## Embedding a Python VM in a Java VM

Using the same techniques used when writing a Python extension of a Java class,
JCC may also be used to embed a Python VM in a Java VM. Following are the steps
and constraints to follow to achieve this:

-
JCC must be built in shared mode.  See [installation instructions](install.html)
for more information about shared mode. Note that for this use on macOS, JCC must
also be built with the link flags _"-framework", "Python"_ in the _LFLAGS_ value.

-
As described in the previous section, define one or more Java classes to be "extended"
from Python to provide the implementations of the native methods declared on them.
Instances of these classes implement the bridges into the Python VM from Java.

-
The _org.apache.jcc.PythonVM_ Java class is going be used from the Java VM's main
thread to initialize the embedded Python VM. This class is installed inside the
JCC egg under the _jcc/classes_ directory and the full path to this directory must
be on the Java _CLASSPATH_.

-
The JCC egg directory contains the JCC shared runtime library - not the JCC Python
extension shared library - but a library called _libjcc.dylib_ on macOS, _libjcc.so_
on Linux or _jcc.dll_ on Windows. This directory must be added to the Java VM's
shared library path via the _-Djava.library.path_ command line parameter.

-
In the Java VM's main thread, initialize the Python VM by calling its static
_start()_ method passing it a Python program name string and optional start-up
arguments in a string array that will be made accessible in Python via _sys.argv_.
Note that the program name string is purely informational, and is not used by the
_start()_ code other than to initialize that Python variable.  This method returns
the singleton PythonVM instance to be used in this Java VM. _start()_ may be called
multiple times; it will always return the same singleton instance.  This instance
may also be retrieved at any later time via the static _get()_ method defined on
the _org.apache.jcc.PythonVM_ class.

-
Any Java VM thread that is going to be calling into the Python VM should start
with acquiring a reference to the Python thread state object by calling
_acquireThreadState()_ method on the Python VM instance. It should then release
the Python thread state before terminating by calling _releaseThreadState()_.
Calling these methods is optional but strongly recommended as it ensures that
Python is not creating and throwing away a thread state everytime the Python VM
is entered and exited from a given Java VM thread.

-
Any Java VM thread may instantiate a Python object for which an extension class
was defined in Java as described in the previous section by calling the
_instantiate()_ method on the PythonVM instance. This method takes two string
parameters, the name of the Python module and the name of the Python class to
import and instantiate from it. The _\_\_init\_\_()_ constructor on this class
must be callable without any parameters and, if defined, must call _super()_ in
order to initialize the Java side. The _instantiate()_ method is declared to return
_java.lang.Object_ but the return value is actually an instance of the Java extension
class used and must be downcast to it.

## Pythonic protocols

When generating wrappers for Python, JCC attempts to detect which classes can be
made iterable:

-
When a class declares to implement _java.lang.Iterable_, JCC makes it iterable
from Python.

-
When a Java class declares a method called _next()_ with no arguments returning
an object type, this class is made iterable. Its _next()_ method is assumed to
terminate iteration by returning _null_.

JCC generates a Python mapping get method for a class when requested to do so via
the _--mapping_ command line option which takes two arguments, the class to generate
the mapping get for and the Java method to use. The method is specified with its name
followed by ':' and its Java
[signature](https://java.sun.com/j2se/1.5.0/docs/guide/jni/spec/types.html#wp16432).

For example, _System.getProperties()['java.class.path']_ is made possible by:

```
--mapping java.util.Properties
        'getProperty:(Ljava/lang/String;)Ljava/lang/String;'
                    # asking for a Python mapping protocol wrapper
                    # for get access on the Properties class by
                    # calling its getProperty method
```

JCC generates Python sequence length and get methods for a class when requested
to do so via the _--sequence_ command line option which takes three arguments,
the class to generate the sequence length and get for and the two java methods
to use. The methods are specified with their name followed by ':' and their Java
[signature](https://java.sun.com/j2se/1.5.0/docs/guide/jni/spec/types.html#wp16432).
For example:

```
for i in xrange(len(hits)):
doc = hits[i]
...
```

is made possible by:
```
--sequence org.apache.lucene.search.Hits
         'length:()I'
         'doc:(I)Lorg/apache/lucene/document/Document;'
```
