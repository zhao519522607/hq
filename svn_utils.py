#!/usr/bin/env python

import os
import re
import sys
import traceback
import datetime

SVN_CMD_COUNT = 2
(_BLAME, _CO_BYDATE) = range(SVN_CMD_COUNT)

SVN_CMDS = {
    _BLAME       :   "svn blame %s",
    _CO_BYDATE   :   "svn co -r '{%s}' %s"
}


# ---------------------------------------------------------
class CodeCounter:
    """
    This class count blank lines, code lines, and comment lines of the
    source files in a directory.
    """
    def __init__(self, top_path, blame = False, ext_list = ['.php', '.py', '.cpp', '.h']):
        try:
            self.path = top_path
            self.blame = blame
            self.ext_list = ext_list
            self.dir_filter = []
            self.file_filter = []
            self.author_dict = dict()

            self.comment_begin = '//'
            self.block_comment_begin = '/\*'
            self.block_comment_end = '\*/'

            self.re_blank = re.compile(r'^\s*$')
            self.re_comment = re.compile(r'^\s*%s\w*' % self.comment_begin)
            self.re_blk_cmt_begin = re.compile(r'^\s*%s\w*' % self.block_comment_begin)
            self.re_blk_cmt_end = re.compile(r'.*%s\s*' % self.block_comment_end)

            self.Clear()
        except:
            print '[ERROR] Exception in CodeCounter::__init__'

    def CheckAuthors(self, filename, author_dict):
        try:
            cmd = SVN_CMDS[_BLAME] % filename
    
            pipe = os.popen(cmd)
            cmd_res = pipe.readlines()
            pipe.close()
    
            for line in cmd_res:
                author = line.split()[1]
                if author_dict.has_key(author):
                    author_dict[author] += 1
                else:
                    author_dict[author] = 1
        except:
            print 'Exception in CheckAuthors()'

    def Clear(self):
        try:
            self.total_lines = 0
            self.num_comment_lines = 0
            self.num_blank_lines = 0
            self.num_code_lines = 0
            self.file_counters = {}
        except:
            print '[ERROR] Exception in CodeCounter::Clear'

    def AddDirFilter(self, dir_pattern_to_skip):
        try:
            self.dir_filter.append(re.compile(r'%s' % dir_pattern_to_skip))
        except:
            print '[ERROR] Exception in CodeCounter::AddDirFilter'

    def AddFileFilter(self, file_pattern_to_skip):
        try:
            self.file_filter.append(re.compile(r'%s' % file_pattern_to_skip))
        except:
            print '[ERROR] Exception in CodeCounter::AddFileFilter'

    def CountFiles(self):
        try:
            if not os.path.isdir(self.path):
                if os.path.exists(self.path): # a specific file
                    for r in self.file_filter:
                        if r.match(self.path):
                            return
                    self.CountLines(self.path)
                    if self.blame:
                        self.CheckAuthors(self.path, self.author_dict)
                else:
                    print '[ERROR] %s is not a valid path or file name!' % self.path
                    return
            for dir, subdirs, files in os.walk(self.path):
                is_filtered = False
                path_tree = dir.split(os.sep)
                for path in path_tree:
                    for r in self.dir_filter:
                        if r.match(path):
                            is_filtered = True
                            break
                if is_filtered:
                    continue
                for file in files:
                    is_skipped = True
                    for ext in self.ext_list:
                        if ext == file[-len(ext):]:
                            if file in self.file_filter:
                                break
                            file = os.path.join(dir, file)
                            self.CountLines(file)
                            if self.blame:
                                self.CheckAuthors(file, self.author_dict)
                            is_skipped = False
                            break
        except:
            print '[ERROR] Exception in CodeCounter::CountFiles'
            print traceback.format_exc()

    def CountLines(self, filename):
        try:
            f = file(filename)
            lines = f.readlines()

            blank_line_cnt = 0
            comment_line_cnt = 0
            code_line_cnt = 0
            in_block_comment = False
            for line in lines:
                if self.re_blank.match(line) or not line:
                    blank_line_cnt += 1
                elif in_block_comment:
                    if self.re_blk_cmt_end.match(line):
                        in_block_comment = False
                    comment_line_cnt += 1
                elif self.re_blk_cmt_begin.match(line):
                    in_block_comment = True
                    comment_line_cnt += 1
                elif self.re_comment.match(line):
                    comment_line_cnt += 1
                else:
                    code_line_cnt += 1

            self.total_lines += (blank_line_cnt + comment_line_cnt + code_line_cnt)
            self.num_blank_lines += blank_line_cnt
            self.num_comment_lines += comment_line_cnt
            self.num_code_lines += code_line_cnt
            self.file_counters[filename] = (code_line_cnt, comment_line_cnt, blank_line_cnt)
        except:
            print '[ERROR] Exception in CodeCounter::CountLines'

    def GetNumCommentLines(self):
        return self.num_comment_lines

    def GetNumBlankLines(self):
        return self.num_blank_lines

    def GetNumCodeLines(self):
        return self.num_code_lines

    def GetNumTotalLines(self):
        return self.total_lines

    def GetFileCounters(self):
        return self.file_counters

    def GetAuthorDict(self):
        return self.author_dict

#  END of class CodeCounter


def _Main():
    '''
    python source_counter.py [path] [blame]
    '''
    try:
        path = './' # default path
        blame = False
        if len(sys.argv) > 1:
            path = sys.argv[1]
            if len(sys.argv) > 2:
                if int(sys.argv[2]):
                    blame = True

        code_cnter = CodeCounter(path, blame)
        code_cnter.AddDirFilter('thirdparty')
        code_cnter.AddDirFilter('\.svn')

        if blame:
            code_cnter.AddFileFilter('.*_pb2.py')

        code_cnter.CountFiles()

        total_lines         = code_cnter.GetNumTotalLines()
        total_code_lines    = code_cnter.GetNumCodeLines()
        total_blank_lines   = code_cnter.GetNumBlankLines()
        total_comment_lines = code_cnter.GetNumCommentLines()

        print '-------------------------------------------------------------------'
        print '         | Total Lines | Code Lines | Comment Lines | Blank Lines |'
        print '-------------------------------------------------------------------'
        print ' ALL     |%9d    |%8d    |%10d     |%9d    ' % (total_lines, total_code_lines, total_comment_lines, total_blank_lines)
        print '-------------------------------------------------------------------'

        if blame:
            code_authors = code_cnter.GetAuthorDict()
            sorted_code_authors = sorted(code_authors.items(), key=lambda x:x[1], reverse=True)
            fd = open('svn_authors.csv', 'w')
            fd.write('Author,Code Lines\n')
            for (author, line_cnt) in sorted_code_authors:
                fd.write('%s,%d\n' % (author, line_cnt))
            fd.close()
            #print 'Author-CodeLines List:\n---------------'
            #for (author, line_cnt) in sorted_code_authors:
            #    print author, line_cnt
            #print '-------------------------------------------------------------------'
    except:
            print 'Exception in _Main()'

if __name__ == '__main__':
    _Main()
