#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import os

def get_file_list(repo, TXN):  
        """svnlook changed -r REV REPOS 获得发生变更的文件 
        """  
        cmd = '%s changed -t %s %s' % (svnlook_bin_path, TXN, repo)  
        output = os.popen(cmd).read()  
        return output

def diff_dir(f_list,my_contxt):
	regex = re.compile(r'\w*%s\w*' %my_contxt)
	result = regex.findall(f_list)
	if result:
		return True
	else:
		return False

if __name__ == '__main__':  
        svnlook_bin_path = '/usr/bin/svnlook'
	file_list = get_file_list(sys.argv[1], sys.argv[2])
	if diff_dir(file_list,'offline/devops'):
		sys.exit(10)
	else:
		pass
