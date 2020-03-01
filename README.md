# Wikoogle
Wikipedia search engine

# Libraries
* https://spacy.io/ seems the most powerful and has a storng community behind it
* https://www.nltk.org/ the library is maintained by a very small number of people and seems like it is buggy, erratic, uneven and difficult to use
* https://whoosh.readthedocs.io/en/latest/intro.html seems dead but is good to do the project. Maybe parsing, tagging, stemming, document preprocessing can be done with this and the searching with a custom implementation. It would be more reasonable since whoosh only support BM25 model  . It is slow that elasticsearch and lucene
* https://lucene.apache.org/solr/ 
* https://elasticsearch-py.readthedocs.io/en/master/

## Tips
* https://wiki.python.org/moin/PythonSpeed/PerformanceTips
* Write high speed functions in C and build a python c extension. Roughly
* Pypy
* Ctypes
* C extension
* I/O performance https://docs.python.org/3/library/io.html

## XML parsing
* http://effbot.org/zone/celementtree.htm
* https://lxml.de/intro.html 
* Wikipedia Schema https://www.mediawiki.org/wiki/Help:Formatting
* https://github.com/attardi/wikiextractor/wiki
## Indexing
* https://www.ibm.com/developerworks/library/x-hiperfparse/index.html 
## Wikitext formatting
* https://en.wikipedia.org/wiki/Help:Wikitext
## Logging
* https://docs.python.org/3/howto/logging-cookbook.html

## Notes 1.0
### Problems
* xml tree memory problem, solved by .clear() and del
* Wikipedia template parsing
###
* How to model the index?
 * Multiple index
   - whoosh index with title and a reference in the wikigoogle index
   - wikigoogle index with the wikipedia parsed template and other information

 
