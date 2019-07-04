# -*- coding: utf-8 -*-
#http://www.nltk.org/_modules/nltk/parse/generate.html
# Natural Language Toolkit: Generating from a CFG
#
# Copyright (C) 2001-2019 NLTK Project
# Author: Steven Bird <stevenbird1@gmail.com>
#         Peter Ljunglöf <peter.ljunglof@heatherleaf.se>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT
#
from __future__ import print_function

import itertools
import sys
from nltk.grammar import Nonterminal
import nltk

def generate(grammar, start=None, depth=None, n=None):
    """
    Generates an iterator of all sentences from a CFG.

    :param grammar: The Grammar used to generate sentences.
    :param start: The Nonterminal from which to start generate sentences.
    :param depth: The maximal depth of the generated tree.
    :param n: The maximum number of sentences to return.
    :return: An iterator of lists of terminal tokens.
    """
    if not start:
        start = grammar.start()
    if depth is None:
        depth = sys.maxsize

    iter = _generate_all(grammar, [start], depth)

    if n:
        iter = itertools.islice(iter, n)

    return iter



def _generate_all(grammar, items, depth):
    if items:
        try:
            for frag1 in _generate_one(grammar, items[0], depth):
                for frag2 in _generate_all(grammar, items[1:], depth):
                    yield frag1 + frag2
        except RuntimeError as _error:
            if _error.message == "maximum recursion depth exceeded":
                # Helpful error message while still showing the recursion stack.
                raise RuntimeError(
                    "The grammar has rule(s) that yield infinite recursion!!"
                )
            else:
                raise
    else:
        yield []


def _generate_one(grammar, item, depth):
    if depth > 0:
        if isinstance(item, Nonterminal):
            for prod in grammar.productions(lhs=item):
                for frag in _generate_all(grammar, prod.rhs(), depth - 1):
                    yield frag
        else:
            yield [item]


demo_grammar = """
    S -> N VP
    VP -> V NP | V NP | V N
    V -> "尊敬"
    N -> "我们" | "老师" | "狗子"
"""
#   Det -> '是' | '一个'
#   N -> 'man' | 'park' | 'dog'
#   P -> 'in' | 'with'

def demo(N=3):
    from nltk.grammar import CFG

    print('Generating the first %d sentences for demo grammar:' % (N,))
    print(demo_grammar)
    grammar = CFG.fromstring(demo_grammar)
    for n, sent in enumerate(generate(grammar, n=N), 1):
        #print(sent)
        print('%3d. %s' % (n, ' '.join(sent)))


    # sent ="Mary saw a dog".split()
    # rd_parser = nltk.RecursiveDescentParser(grammar)

    # for tree in rd_parser.nbest_parse(sent):
    #     print (tree)

    # # Make your POS sentence into a list of tokens.
    # sentence ="尊重 我们 吧".split(" ")


    # # Load the grammar into the ChartParser.
    # cp = nltk.ChartParser(demo_grammar)

    # # Generate and print the nbest_parse from the grammar given the sentence tokens.
    # for tree in cp.nbest_parse(sentence):
    #     print (tree)
if __name__ == '__main__':
    demo()