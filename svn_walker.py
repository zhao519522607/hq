#!/usr/bin/env python

import os
import sys
import datetime
from svn_utils import *

SVN_URL = 'svn://url'

ONE_DAY = datetime.timedelta(days=1)

TODAY = datetime.date.today()
SWITCH_DATE = datetime.datetime(2010, 12, 04).date()

BEGIN_DATE = datetime.datetime(2010, 11, 16).date()
END_DATE = TODAY

CO_CMD = "svn co -r '{%s}' %s"
RM_CMD = "rm -rf ./src"
OUTPUT_FILE = 'svn_code_lines.csv'
OUTPUT_HEADER = 'Date,Code Lines,Comment Lines,UT Lines\n'

def CheckOutCodeByDate(date):
    try:
        print 'Checking out code on date', str(date)
        url = SVN_URL[0]

        # Check out code by date
        cmd = CO_CMD % (str(date), url)
        pipe = os.popen(cmd)
        cmd_res = pipe.readlines()
        pipe.close()
        #os.system(cmd)
    except:
        print 'Exception in CheckOutCodeByDate()!'

def CountCodeLines(date, fd):
    try:
        try:
            path = './src'
            code_cnter = CodeCounter(path)
            code_cnter.AddDirFilter('thirdparty')
            code_cnter.AddDirFilter('\.svn')
            code_cnter.AddFileFilter('.*_pb2.py')

            code_cnter.CountFiles()
        except:
            print 'Exception in running the counters!'
            return

        total_lines         = code_cnter.GetNumTotalLines()
        total_comment_lines = code_cnter.GetNumCommentLines()

        line = date + ',' + str(total_lines_wo_ut - total_comment_lines_wo_ut) + ','\
             + str(total_comment_lines_wo_ut) + ',' + str(ut_total_lines) + '\n'
        fd.write(line)
        fd.flush()
    except:
        print 'Exception in CountCodeLines()!'

def _Main():
    try:
        os.system(RM_CMD)
        fd = open(OUTPUT_FILE, 'w')
        fd.write(OUTPUT_HEADER)

        date = BEGIN_DATE
        while (END_DATE - date).days >= 0:
            CheckOutCodeByDate(date)
            CountCodeLines(str(date), fd)
            date += ONE_DAY

        fd.close()
        os.system(RM_CMD)
    except:
        print 'Exception in _Main()!'

if __name__ == '__main__':
    _Main()
