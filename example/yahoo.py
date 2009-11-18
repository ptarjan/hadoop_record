#!/usr/bin/env python
"""
Takes a line of hadoop record csv encoded data and returns a Document

>>> import yahoo
>>> line = "http://www.paulisageek.com\t'http://www.paulisageek.com,#656e,1234567890"
>>> doc = yahoo.Document(line)
>>> print doc.url, doc.language, doc.lastCrawlTime
"""
import sys
sys.path.append("hadoop_record.mod")
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
