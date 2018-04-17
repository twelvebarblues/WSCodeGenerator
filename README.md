# WSCodeGenerator
This project generates a web server and code that handles a given set of URIs.

The code is generated from a URI file and a set of templates.  The URI file contains lines formatted like:
> GET/example/\<param\>/test

Each line is parsed into a regular expression, that is put into an STL map that maps a regex wrapper object to a generated function. Variables are represented by the string literal __\<param\>__. Unlike frameworks like [Flask](http://flask.pocoo.org/), where one function can handle multiple HTTP verbs, this code generates a seperate function for each GET/PUT/POST/DELETE specified for the same URI.

The templates contain three keys expected by ws_generator.py, __functions__, __function_prototypes__ and __urlMap__. The keys are specified in the templates using python syntax, for example, __%(urlMap)s__. These keys are populated by the ws_generator.py, which contains a template string for each of the keys. The webserver is implemented using the [Poco](https://pocoproject.org/) libraries, but some other library could be used by changing the template strings in ws_generator.py and the corresponding code the template files.

## System Requirements
This code was developed on Ubuntu 16.04 using the following:
* [Poco 1.9.0](https://pocoproject.org)
* G++ 5.4.0
* Python 3.5.2

## Building
To generate and run the example code  (CMakeLists.txt only works with the example):
```
you@home:~/dev/ws_generate$ ls
CMakeLists.txt  examples  README.md  templates  ws_generate.py
you@home:~/dev/ws_generate$ python ws_generate.py 
you@home:~/dev/ws_generate$ ls
CMakeLists.txt  examples  include  README.md  src  templates  ws_generate.py
you@home:~/dev/ws_generate$ mkdir build 
you@home:~/dev/ws_generate$ cd build/
you@home:~/dev/ws_generate$ cmake ..
-- The C compiler identification is GNU 5.4.0
-- The CXX compiler identification is GNU 5.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/mjones/dev/tmp/ws2/gen/build
you@home:~/dev/ws_generate$ make
Scanning dependencies of target webserver
[ 33%] Building CXX object CMakeFiles/webserver.dir/src/WebService.cpp.o
[ 66%] Building CXX object CMakeFiles/webserver.dir/src/WebServiceFunctions.cpp.o
[100%] Linking CXX executable webserver
[100%] Built target webserver
you@home:~/dev/ws_generate$ ./webserver 

```
## Options
There are options to specify where the URIs, templates and generated code exist:
```
you@home:~/dev/ws_generate$ python ws_generate.py --help
usage: ws_generate.py [-h] [--uris URIS] [--templates TEMPLATES]
                      [--source_dest SOURCE_DEST] [--header_dest HEADER_DEST]

Generate code for a simple web server that handles a given set of URIs.

optional arguments:
  -h, --help            show this help message and exit
  --uris URIS           file containing URIs for code generation (default: examples/uris.txt)
  --templates TEMPLATES
                        directory containing templates (default: templates)
  --source_dest SOURCE_DEST
                        directory where source files will be generated (default: src)
  --header_dest HEADER_DEST
                        directory where header files will be generated (default: include)

Example:
    ws_generate.py --uris ./my_uris_file --templates my_template_dir
```
