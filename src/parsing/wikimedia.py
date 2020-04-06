from io import StringIO
import re
import logging

logger = logging.getLogger('Wikimedia')

'''
http://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/
Every now and then, I stumble onto some algorithm or idea that’s so clever and such a perfect solution to a problem that I feel like I got smarter or gained a new superpower just by learning it. Heaps (just about the only thing I got out of my truncated CS education) were one thing like this. I recently stumbled onto another: Pratt parsers.

When you’re writing a parser, recursive descent is as easy as spreading peanut butter. It excels when you can figure out what to do next based on the next chunk of code you’re parsing. That’s usually true at the top level of a language where things like classes are and also for statements since most start with something that uniquely identifies them (if, for, while, etc.).

But it gets tricky when you get to expressions. When it comes to infix operators like +, postfix ones like ++, and even mixfix expressions like ?:, it can be hard to tell what kind of expression you’re parsing until you’re halfway through it. You can do this with recursive descent, but it’s a chore. You have to write separate functions for each level of precedence (JavaScript has 17 of them, for example), manually handle associativity, and smear your grammar across a bunch of parsing code until it’s hard to see.
'''
''' Ignore character '''


class Wikimedia:

    def __init__(self, text):
        self._text = text
        self._pos = -1
        self._len = len(text) - 1

    def compile(self, text, block_size=None, ):
        pass
