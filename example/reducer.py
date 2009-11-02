#!/usr/bin/env python
import sys

word2count = {}

for line in sys.stdin:
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        count = int(count)
        word2count[word] = word2count.get(word, 0) + count
    except ValueError:
        pass

sorted_word2count = word2count.items()
sorted_word2count.sort(lambda x,y : y[1] - x[1])

for word, count in sorted_word2count:
    print '%s\t%s'% (word, count)
