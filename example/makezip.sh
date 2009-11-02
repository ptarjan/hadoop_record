#!/bin/sh

find hadoop_record -name '*.pyc' -exec rm {} \;
zip hadoop_record.mod hadoop_record/*.py hadoop_record/ply/*.py
