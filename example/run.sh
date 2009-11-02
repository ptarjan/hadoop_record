#!/bin/sh
cat sample.txt | ./mapper.py | sort | ./reducer.py
