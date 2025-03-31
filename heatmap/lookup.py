#!/usr/bin/env python
#
# Program:      $Id$
# Author:       Robert Beverly <rbeverly@nps.edu>
# Description:  Read MRT, IPv6 to prefix
#               Fetch MRT files from, e.g.,: http://archive.routeviews.org/route-views6/bgpdata/2020.09/RIBS/rib.20200920.1200.bz2
#               ./lookup.py -i rib.20200920.1200.bz2 -l forBGPLookup.txt

from mrtparse import *
import argparse
import radix
import bz2
import sys


def build(rtree, infile):
  fd = bz2.BZ2File(infile, 'rb')
  r = Reader(fd)
  while True:
    try: 
      m = r.next()  
    except StopIteration:
      break
    m = m.mrt
    if m.err: continue
    if (m.type == MRT_T['TABLE_DUMP_V2'] and
      (m.subtype == TD_V2_ST['RIB_IPV6_UNICAST'] )
      ):
      prefix = m.rib.prefix + '/' + str(m.rib.plen)
      for i in range(len(m.rib.entry)):
        entry = m.rib.entry[i]
        aspath = ""
        for attr in entry.attr:
          if attr.type == BGP_ATTR_T['AS_PATH']:
            aspath = " ".join(attr.as_path[0]['val'])
            if len(attr.as_path[0]['val']) > 0:
              origin = attr.as_path[0]['val'][-1]
      if prefix != '::/0':
        #print("prefix:", prefix, "Origin:", origin)
        rnode = rtree.add(prefix)
        rnode.data['asn'] = int(origin)

def lookup(rtree, infile):
  for line in open(infile):
    ip = line.strip()
    rnode = rtree.search_best(ip) 
    prefix = '::0/0'
    asn = -1
    if (rnode):
      prefix = rnode.prefix
      asn = rnode.data['asn']
    print("%s,%s,%d" % (ip, prefix, asn))
      

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--input", required=True, help='Input MRT')
  parser.add_argument("-l", "--lookup", required=True, help='IPv6 to lookup')
  args = parser.parse_args()

  rtree = radix.Radix()
  build(rtree, args.input)
  lookup(rtree, args.lookup) 
