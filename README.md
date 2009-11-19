# hadoop_record : A python record reader for hadoop

This library reads the output of [Hadoop CSV](http://svn.apache.org/viewvc/hadoop/common/trunk/src/java/org/apache/hadoop/record/CsvRecordOutput.java) files so you can easily use them in python streaming programs.

## tl;dr

    git clone git@github.com:ptarjan/hadoop_record.git
    cd hadoop_record/example/
    cat sample.txt | ./mapper.py | sort | ./reducer.py
     en      2
     ru      1

## Features

* Decodes hadoop jute records
* Doesn't docode strings until they are used (good for large data sets when you only care about a part of it)

## Command line Example

    >>> from hadoop_record import csv
    >>> csv("T")
    True
    >>> csv(";-1234")
    -1234
    >>> csv("1.0E-10")
    1e-10
    >>> csv("s{T,F}")
    [True, False]
    >>> csv("v{T,F}")
    [True, False]
    >>> csv("v{s{T,F}}")
    [[True, False]]
    >>> csv("m{'don't,#73746f70}")
    {LazyString("don't"): LazyString('stop')}
    >>> csv("'\xe2\x98\x83")
    LazyString('\xe2\x98\x83')
    >>> str(csv("'\xe2\x98\x83"))
    '\xe2\x98\x83'
    >>> unicode(csv("'\xe2\x98\x83"))
    u'\u2603'
    >>> csv("'%00%0a%25%2c")
    LazyString('\x00\n%,')

## Hadoop

    git clone git@github.com:ptarjan/hadoop_record.git
    cd hadoop_record/example/
    hadoop fs -put sample.txt
    hadoop jar $HADOOP_HOME/hadoop-streaming.jar -input hadoop_record/sample.txt -inputformat TextInputFormat -output hadoop_record/sample_output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py -file yahoo.py -file hadoop_record.mod
    hadoop fs -cat hadoop_record/sample_output
     en      2
     ru      1

And if you have a binary record, you need:

    -inputformat SequenceFileAsTextInputFormat -file JuteRecordClasses.jar

and you're good to go. Like

    $ hadoop jar $HADOOP_HOME/hadoop-streaming.jar -input /data/logs_in_jute_format/part-0* -inputformat SequenceFileAsTextInputFormat -output output_dir -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py -file yahoo.py -file JuterecordClasses.jar -file hadoop_record.mod

With `mapper.py`, `reducer.py`, and `yahoo.py` from the `examples` directory.
