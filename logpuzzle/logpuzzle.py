#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import urlparse

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # hostname = filename after the underscore
  match = re.search(r'(_)(.+)', filename)
  if not match:
    print 'invalid filename'
    return []

  hostname = match.group(2)

  urllist = []

  try:
    f = open(filename, 'r')
    for line in f:
      # get path
      match = re.search(r'(GET )(\S*)( HTTP)', line)
      if match:
        path = match.group(2)
        # if string puzzle appears in path, build full url and add to list
        if path.find('puzzle') != -1:
          url = urlparse.urljoin('http://' + hostname, path)
          #print 'url: ' + url
          if url not in urllist:
            urllist.append(url)
    f.close()
  except IOError:
    sys.stderr.write('problem reading ' + filename)
  
  return sorted(urllist, key=custom_sort_helper)
  
def custom_sort_helper(url):
  #if url is in -wordchars-wordchars.jpg form, return second wordchar
  # else return entire url
  match = re.search(r'-\w*-(\w*).jpg$', url)
  if match:
    return match.group(1)
  else :
    return url

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  f = open(os.path.join(dest_dir, 'index.html'), 'w')
  f.write('<verbatim>\n<html>\n<body>\n') #write instead of append
  i = 0
  while i < len(img_urls):
    print 'Retrieving img' + str(i)
    path = os.path.join(dest_dir, 'img' + str(i))
    # retrieve image slice and save to path
    urllib.urlretrieve(img_urls[i], path)
    # write the reference to that path in our html file
    f.write('<img src="' + os.path.abspath(path) + '">')
    i = i + 1

  f.write('\n</body>\n</html>')
  f.close()
  

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
