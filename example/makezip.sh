#!/bin/sh

# builds a zip file to easily distribute on hadoop
#
# must be named .mod instead of .zip beacuse hadoop
# decompresses .zip on its own and puts it in a funky
# directory

find hadoop_record -name '*.pyc' -exec rm {} \;
zip hadoop_record.mod hadoop_record/*.py hadoop_record/ply/*.py
