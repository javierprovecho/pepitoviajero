#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 rguerra <rguerra@moxie>
#
# Distributed under terms of the MIT license.

"""

"""
from collections import defaultdict
import random
import sys
from pprint import pprint, pformat
def weighted_choice(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)
        self.weighted_prod = defaultdict(list)
    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))
        uniform_weight = 100.0/float(len(self.prod[lhs]))
        self.weighted_prod[lhs] = [uniform_weight]*len(self.prod[lhs])
    def add_weighted_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP$0.5 PP$0.5')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for w_prod in prods:
            prod, weight = w_prod.split("$")
            self.prod[lhs].append(tuple(prod.split()))
            self.weighted_prod[lhs].append(float(weight))
    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '

        return sentence
    def gen_random_convergent(self,
          symbol,
          cfactor=0.25,
          pcount=defaultdict(int)
      ):
          """ Generate a random sentence from the
              grammar, starting with the given symbol.

              Uses a convergent algorithm - productions
              that have already appeared in the
              derivation on each branch have a smaller
              chance to be selected.

              cfactor - controls how tight the
              convergence is. 0 < cfactor < 1.0

              pcount is used internally by the
              recursive calls to pass on the
              productions that have been used in the
              branch.
          """
          sentence = ''

          # The possible productions of this symbol are weighted
          # by their appearance in the branch that has led to this
          # symbol in the derivation
          #
          try:
              weights = self.weighted_prod[symbol]
              """
              print '/******* 11111 *******/'
              print symbol
              print self.prod[symbol]
              print weights
              print weighted_choice(weights)
              print '/**************/\n'
              """
              rand_prod = self.prod[symbol][weighted_choice(weights)]
          except:
                try:
                    weights = []
                    for prod in self.prod[symbol]:
                        if prod in pcount:
                            weights.append(cfactor ** (pcount[prod]))
                        else:
                            weights.append(1.0)
                    """
                    print '/******* 222222 *******/'
                    print symbol
                    print self.prod[symbol]
                    print weights
                    print weighted_choice(weights)
                    print '/**************/\n'
                    """
                    rand_prod = self.prod[symbol][weighted_choice(weights)]
                except:
                    rand_prod = random.choice(self.prod[symbol])
          # pcount is a single object (created in the first call to
          # this method) that's being passed around into recursive
          # calls to count how many times productions have been
          # used.
          # Before recursive calls the count is updated, and after
          # the sentence for this call is ready, it is rolled-back
          # to avoid modifying the parent's pcount.
          #
          pcount[rand_prod] += 1

          for sym in rand_prod:
              # for non-terminals, recurse
              if sym in self.prod:
                  sentence += self.gen_random_convergent(
                                      sym,
                                      cfactor=cfactor,
                                      pcount=pcount)
              else:
                  sentence += sym + ' '

          # backtracking: clear the modification to pcount
          pcount[rand_prod] -= 1
          return sentence

if __name__ == "__main__":
    emociones = ['enfadado', 'asqueado', 'triste', 'alegre', 'apagado', 'encendido']
    emocion = 'enfadado'
    for i in xrange(100):
        print "\t",generateEmoticon(emocion)
