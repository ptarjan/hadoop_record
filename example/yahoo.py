#!/usr/bin/env python
import sys
sys.path.append("hadoop.mod")
from hadoop_record import parser

class Document:
    def __init__(self, line):
        if line.find("\t") == -1 :
            raise Exception("No Tab. Isn't this supposed to be key\\tval?")
        self.key, remain = line.split("\t", 1)
        if remain == "\n" or remain == "" :
            raise Exception("No value for key")
        p = parser.csv(remain)
        self.url, self.language, self.lastCrawlTime = p[0:3]

        ### decode all of p to actual keys and values using the schema

        self._parsed = p
