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

## Wikimedia parsing
* https://www.mediawiki.org/wiki/Markup_spec/EBNF
* https://github.com/attardi/wikiextractor/wiki


## Indexing
* https://www.ibm.com/developerworks/library/x-hiperfparse/index.html 
## Wikitext formatting
* https://en.wikipedia.org/wiki/Help:Wikitext
* https://en.wikipedia.org/wiki/Help:Cheatsheet
* https://en.wikiquote.org/wiki/Help:Wiki_markup_examples	
* https://dl.acm.org/doi/10.1145/512927.512931
* https://tomassetti.me/guide-parsing-algorithms-terminology/#structureParser

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

## Notes 1.1
* Wikimedia markup spec
 * Keep &ltmath; and &gt/math to show math expressions or remove them?;
   -> Everything different from Wikimedia markspec should be kept or handle situation case by case?
      For indexing purpose these expression are quite useless since they need to be processed (ex. MathJax, Latex ec..)

## Notes 1.2
* Parser works, it might be useful to build a secondary index with a parsed wikitext to add features like this https://www.google.com/search?q=Known+star+systems+within+5.0+parsecs+(16.3+light-years)&rlz=1C1CHBF_enIT883IT883&oq=Known+star+systems+within+5.0+parsecs+(16.3+light-years)&aqs=chrome..69i57.182j0j7&sourceid=chrome&ie=UTF-8 (Table rendered directly)

## Notes 1.3
Things to do:
* UI
 * Nodejs/Flask that serves a SPA/SSR
* Searching
 * Query expansion

## Notes 1.4
* Summarize with RAKE https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents
* Query expansion and WSD with NLTK
 - An idea might be use wikipedia articles Category references to build a wikipedia-specific thesaurus to get better results
	 


# Snippet generation
* https://arxiv.org/pdf/2002.10782.pdf
* http://marksanderson.org/publications/my_papers/SIGIR98.pdf

# WSD and Query expansion
* https://arxiv.org/pdf/1105.5444.pdf
* http://disi.unitn.it/~bernardi/Courses/DL/Slides_11_12/9.pdf
* https://dl.acm.org/doi/pdf/10.1145/333135.333138#:~:text=Local%20context%20analysis%20ranks%20the,query%20expansion%20than%20existing%20techniques.