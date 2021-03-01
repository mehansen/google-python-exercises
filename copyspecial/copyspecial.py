#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

def get_special_paths(dirs):
  # part A
  # for all dirs, get files in dir
  # filter for those that are special
  paths = []
  for di in dirs:
    filenames = os.listdir(di)
    for name in filenames:
      match = re.search(r'__\w+__', name)
      if match:
        paths.append(os.path.abspath(os.path.join(di, name)))
  return paths


def copy_to(paths, di):
  # part b
  if not os.path.exists(di):
    os.makedirs(di)
  for path in paths:
    shutil.copy(path, di)

def zip_to(paths, zipfile):
  # part c
  cmd = 'zip -j ' + zipfile
  for path in paths:
    cmd = cmd + ' ' + path.replace(' ', r'\ ')
  print "running external command: " + cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  paths = get_special_paths(args)

  if todir != '':
    copy_to(paths, todir)
  if tozip != '':
    zip_to(paths, tozip)
  if todir == '' and tozip == '':
    for path in paths:
      print path


  
if __name__ == "__main__":
  main()
