#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, commands

if len(sys.argv) < 2 or sys.argv[1] is None:
    print "use sample:python kill.py command"
    exit()

comand = sys.argv[1].strip()

rs = commands.getoutput("ps -ef|grep %s|awk '{print $2}'" % comand)
rs = rs.strip().split("\n")
rs = ' '.join(rs)
print 'to kill:%s' % rs
rs = commands.getoutput("kill -9 %s" % rs)
print rs
