#! /usr/bin/env python
# -*- coding: utf8 -*-
#Author: zyb

import commands
import traceback
import os

def file_r():
    with open('/tmp/oom_file','r') as f:
        before_context = ''.join(f.readlines())
    return before_context

def file_w():
    (status, output) = commands.getstatusoutput('egrep "Out of memory" /var/log/messages |grep -v grep')
    with open('/tmp/oom_file','w+') as f:
        f.write(output)
    return output

if __name__ == '__main__':
    try:
        if os.path.exists('/tmp/oom_file'):
            a = file_r()
            b = file_w()
            if b.strip() == "":
                print 0
            else:
                if a != b:
                    print 1
                else:
                    print 0
        else:
            b = file_w()
            if b.strip() != "":
                print 1
            else:
                print 0
    except:
        print "Except Error:%s" % traceback.format_exc()
