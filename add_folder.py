import os
import add_file
import glob
import sys
for file in glob.glob(os.path.abspath(os.path.expanduser(sys.argv[1]))+"/**",recursive=True):
    add_file.add("test1.py",file)
