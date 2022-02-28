#!/usr/bin/env python

import pycurl
import json
import io
import prettytable
import argparse
import textwrap
import os.path
import time

DESCRIPTION=r"""Obtain cookie with:

  cern-get-sso-cookie --cert ~/.globus/usercert.pem        \
                      --key  ~/.globus/userkey.pem         \
                      -u https://cms-gen-dev.cern.ch/xsdb/ \
                      -o cookie.txt

When the output is too wide, pipe it into less -S like so:

  inspect_xsdb.py -i <dbs name> | less -S

Example:
  inspect_xsdb.py -i TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8
"""

KEYS = [
  "process_name", "status", "isValid", "cross_section", "total_uncertainty", "other_uncertainty", "accuracy",
  "contact", "DAS", "MCM", "equivalent_lumi", "fraction_negative_weight", "reweighting", "cuts", "kFactor",
  "shower", "matrix_generator", "energy", "comments", "refs", "discussion", "modifiedOn", "createdOn",
  "modifiedBy", "approvedBy", "createdBy",
]

DELIMITER = ';'

# https://stackoverflow.com/a/64102901/4056193
class RawFormatter(argparse.HelpFormatter):
  def _fill_text(self, text, width, indent):
    return '\n'.join([ textwrap.fill(line, width) for line in textwrap.dedent(text).splitlines() ])

class XSDB:
  def __init__(self, cookie):
    self.url = 'https://cms-gen-dev.cern.ch/xsdb/api/search'
    self.header = [
      'Content-Type:application/json',
      'Accept:application/json',
    ]
    self.cookie = cookie
    self.max_retries = 3

    if not os.path.isfile(self.cookie):
      raise RuntimeError("Cookie not found: %s" % self.cookie)

  def get(self, query):
    buf = io.BytesIO()
    nof_retries = 0
    while nof_retries < self.max_retries:
      c = pycurl.Curl()
      c.setopt(pycurl.FOLLOWLOCATION, 1) # -L
      c.setopt(pycurl.COOKIEJAR, self.cookie)
      c.setopt(pycurl.COOKIEFILE, self.cookie)
      c.setopt(pycurl.HTTPHEADER, self.header) # -H
      c.setopt(pycurl.VERBOSE, 0) # -s
      c.setopt(c.WRITEDATA, buf)
      c.setopt(c.URL, self.url)
      c.setopt(pycurl.POST, 1) # -X POST
      c.setopt(c.POSTFIELDS, json.dumps(query)) # -d
      try:
        c.perform()
        assert (c.getinfo(pycurl.RESPONSE_CODE) == 200)
        c.close()
        break
      except BaseException as e:
        nof_retries += 1
        time.sleep(nof_retries**2)
    body = buf.getvalue().decode('utf-8')
    data = json.loads(body) if body else None
    return data

def print_data(data, header, do_table):
  assert(all(col_name in KEYS for col_name in header))
  if data:
    if do_table:
      table = prettytable.PrettyTable()
      table.field_names = header
      for entry in data:
        table.add_row([ entry[col] if col in entry else '' for col in header ])
      print(table)
    else:
      rows = []
      for entry in data:
        rows.append(DELIMITER.join([ entry[col] if col in entry else '' for col in header ]))
      print('\n'.join(rows))
  return None

def parse_arguments():
  DEFAULT_KEYS = [
    'process_name', 'cross_section', 'total_uncertainty', 'accuracy', 'energy', 'comments', 'refs',
  ]
  def bool_type(s):
    return s.lower() in ['true', 't', 'yes', '1']

  parser = argparse.ArgumentParser(description = DESCRIPTION, formatter_class = RawFormatter)
  parser.add_argument('-i', '--input', dest = 'input', metavar = 'name', required = True, type = str,
                      help = 'DBS name (or first first part of it)')
  parser.add_argument('-k', '--keys', dest = 'keys', metavar = 'key', required = False, type = str, nargs = '+',
                      default = DEFAULT_KEYS, choices = KEYS,
                      help = 'Keys to print')
  parser.add_argument('-a', '--accuracy', dest = 'accuracy', metavar = 'order', required = False, type = str, default = '',
                      help = 'Accuracy (eg NLO)')
  parser.add_argument('-e', '--energy', dest = 'energy', metavar = 'number', required = False, type = float, default = 0.,
                      help = 'Center-of-momentum energy')
  parser.add_argument('-c', '--cookie', dest = 'cookie', metavar = 'path', required = False, type = str, default = 'cookie.txt',
                      help = 'Cookie')
  parser.add_argument('-t', '--table', dest = 'table', metavar = 'flag', required = False, type = bool_type, default = True,
                      help = 'Print table')
  args = parser.parse_args()

  return args

def construct_query(args):
  dbs_name = args.input
  if dbs_name.startswith('/'):
    dbs_name_split = dbs_name.split('/')
    if len(dbs_name_split) != 4:
      raise RuntimeError("Invalid DBS name: %s" % dbs_name)
    dbs_name = dbs_name_split[1]
  query = {
    'DAS': dbs_name,  # DAS is alias for process_name
  }
  if args.accuracy:
    query.update({
      'accuracy' : args.accuracy,
    })
  if args.energy > 0:
    query.update({
      'energy' : str(int(args.energy) if args.energy.is_integer() else args.energy),
    })
  return query

if __name__ == '__main__':
  args = parse_arguments()
  query = construct_query(args)
  xsdb = XSDB(args.cookie)
  results = xsdb.get(query)
  print_data(results, args.keys, args.table)
