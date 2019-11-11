Title: Features
URL: pylucene/features.html
save_as: pylucene/features.html
template: lucene/pylucene/page
slug: pylucene-features

## Warning

Before calling any PyLucene API that requires the Java VM, start it by
calling _initVM(classpath, ...)_. More about this function in [here](jcc/features.html).

## Installing PyLucene

PyLucene is a Python extension built with [JCC](jcc/).

To build PyLucene, JCC needs to be built first. Sources for JCC are
included with the PyLucene sources. Instructions for building and
installing JCC are [here](jcc/install.html).

Instruction for building PyLuceneare [here](install.html).

## API documentation

PyLucene is closely tracking Java
Lucene<span style="vertical-align: super; font-size: xx-small">TM</span> releases.
It intends to supports the entire Lucene API.


PyLucene also includes a number of Lucene contrib packages: the Snowball analyzer
and stemmers, the highlighter package, analyzers for other languages than English,
regular expression queries, specialized queries such as 'more like this' and more.

This document only covers the pythonic extensions to Lucene offered
by PyLucene as well as some differences between the Java and Python
APIs. For the documentation on Java Lucene APIs,
see [here](https://lucene.apache.org/java/docs/api/index.html).

To help with debugging and to support some Lucene APIs, PyLucene also
exposes some Java runtime APIs.

## Samples

The best way to learn PyLucene is to look at the samples and tests included with
the PyLucene source release or on the web at:

- [https://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/samples](https://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/samples)
- [https://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/test](https://svn.apache.org/viewcvs.cgi/lucene/pylucene/trunk/test)

## Threading support with attachCurrentThread

Before PyLucene APIs can be used from a thread other than the main thread that was
not created by the Java Runtime, the _attachCurrentThread()_ method must be
called on the _JCCEnv_ object returned by the _initVM()_ or _getVMEnv()_ functions.

## Exception handling with lucene.JavaError

Java exceptions are caught at the language barrier and reported to Python by raising
a JavaError instance whose args tuple contains the actual Java Exception instance.

## Handling Java arrays

Java arrays are returned to Python in a _JArray_ wrapper instance that
implements the Python sequence protocol. It is possible to change array elements
but not to change the array size.

A few Lucene APIs take array arguments and expect values to be returned in them.
To call such an API and be able to retrieve the array values after the call, a
Java array needs to instantiated first.<br/> For example, accessing termDocs:

```
termDocs = reader.termDocs(Term("isbn", isbn))<br/>
docs = JArray('int')(1)   # allocate an int[1] array<br/>
freq = JArray('int')(1)   # allocate an int[1] array<br/>
if termDocs.read(docs, freq) == 1:<br/>
&nbsp;&nbsp;bits.set(docs[0])     # access the array's first element<br/>
```
In addition to _int_, the _JArray_ function accepts _object_, _string_,
_bool_, _byte_, _char_, _double_, _float_, _long_ and _short_ to create an array
of the corresponding type. The _JArray('object')_ constructor takes a second
argument denoting the class of the object elements. This argument is optional and
defaults to Object.

To convert a char array to a Python string use a _''.join(array)_ construct.

Instead of an integer denoting the size of the desired Java array, a sequence of
objects of the expected element type may be passed in to the array constructor.<br/>
For example:

```
\# creating a Java array of double from the [1.5, 2.5] list<br/>
JArray('double')([1.5, 2.5])<br/>
```
All methods that expect an array also accept a sequence of Python objects of the
expected element type. If no values are expected from the array arguments after
the call, it is hence not necessary to instantiate a Java array to make such calls.

See [JCC](jcc/features.html) for more information about handling arrays.

## Differences between the Java Lucene and PyLucene APIs

- The PyLucene API exposes all Java Lucene classes in a flat namespace in the
PyLucene module. For example, the Java import statement
`import org.apache.lucene.index.IndexReader;` corresponds to the Python import
statement `from lucene import IndexReader`

- Downcasting is a common operation in Java but not a concept in Python. Because
the wrapper objects implementing exactly the APIs of the declared type of the
wrapped object, all classes implement two class methods called instance_ and
cast_ that verify and cast an instance respectively.

## Phythonic extensions to the Java Lucene APIs

Java is a very verbose language. Python, on the other hand, offers many
syntactically attractive constructs for iteration, property access, etc... As
the Java Lucene samples from the _Lucene in Action_ book were ported to Python,
PyLucene received a number of pythonic extensions listed here:

- Iterating search hits is a very common operation. Hits instances are iterable
in Python. Two values are returned for each iteration, the zero-based number of
the document in the Hits instance and the document instance itself.<br/>
The Java loop:
```
for (int i = 0; i &lt; hits.length(); i++) {<br/>
&nbsp;&nbsp;Document doc = hits.doc(i);<br/>
&nbsp;&nbsp;System.out.println(hits.score(i) + " : " + doc.get("title"));<br/>
}<br/>
```

can be written in Python:

```
for hit in hits:<br/>
&nbsp;&nbsp;hit = Hit.cast_(hit)<br/>
&nbsp;&nbsp;print hit.getScore(), ':', hit.getDocument['title']<br/>
```

if hit.iterator()'s next() method were declared to return _Hit_ instead of
_Object_, the above cast_() call would not be unnecessary.<br/> The same java
loop can also be written:

```
for i xrange(len(hits)):<br/>
&nbsp;&nbsp;print hits.score(i), ':', hits[i]['title']<br/>
```

- Hits instances partially implement the Python 'sequence' protocol.<br/>
The Java expressions:

```
hits.length();<br/>
doc = hits.get(i);<br/>
```

are better written in Python:

```
len(hits)<br/>
doc = hits[i]<br/>
```

- Document instances have fields whose values can be accessed through the mapping
protocol.<br/> The Java expression:

```
doc.get("title")
```

is better written in Python:

```
doc['title']
```

- Document instances can be iterated over for their fields.<br/> The Java loop:

```
Enumeration fields = doc.getFields();<br/>
while (fields.hasMoreElements()) {<br/>
&nbsp;&nbsp;Field field = (Field) fields.nextElement();<br/>
&nbsp;&nbsp;...<br/>
}<br/>
```

is better written in Python:

```
for field in doc.getFields():<br/>
&nbsp;&nbsp;field = Field.cast_(field)<br/>
&nbsp;&nbsp;...<br/>
```

Once JCC heeds Java 1.5 type parameters and once Java Lucene makes use of them,
such casting should become unnecessary

## Extending Java Lucene classes from Python

Many areas of the Lucene API expect the programmer to provide their own implementation
or specialization of a feature where the default is inappropriate. For example,
text analyzers and tokenizers are an area where many parameters and environmental
or cultural factors are calling for customization.

PyLucene enables this by providing Java extension points listed below that serve
s proxies for Java to call back into the Python implementations of these customizations.

These extension points are simple Java classes that JCC generates the native C++
implementations for. It is easy to add more such extensions classes into the
'java' directory of the PyLucene source tree.

To learn more about this topic, please refer to the JCC [documentation](jcc/features.html).

Please refer to the classes in the 'java' tree for currently available extension
points. Examples of uses of these extension points are to be found in PyLucene's
unit tests.
