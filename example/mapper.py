#!/usr/bin/env python
import sys
import yahoo

for line in sys.stdin :
    if line.strip() == "" : continue
    try :
        doc = yahoo.Document(line)
    except Exception, why:
        sys.stderr.write("%s - %s\n" % (str(why), line[:100]))
        continue

    print "%s\t%s" % (doc.language, 1)
