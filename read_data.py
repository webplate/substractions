#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, os, re
from parameters import *

def read_datafile(filename):
    '''Return content from datafile of subject'''
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            out = []
            for row in reader:
                #ignore comments
                if row[0][0] != '#':
                    r = []
                    for item in row:
                        r.append(item)
                    if len(r) > 0 :
                        out.append(r[0])
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    return out

def list_files(path, pattern):
    '''Returns a list of filepaths to access subjects data
    '''
    files = []
    for dirPath,dirNames,filName in os.walk(path):
        for theFile in filName:
            #list only subject datafiles
            if re.match(subject_pattern, theFile) :
                files.append(os.path.join(dirPath,theFile))
    return files

def data_set(path, pattern):
    '''Returns a list of dictionnaries, one for each subject
    '''
    data = []
    files_p = list_files(dataPath, pattern)
    for p in files_p :
        results = read_datafile(p)
        #keep only non empty datafiles
        if len(results) > 0 :
            data.append({'path' : p, 'results' : results})
    return data

def read_subfile(filename):
    '''Return list of subtractions (d1-d2 as [d1, d2])'''
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter='-')
        try:
            out = []
            for row in reader:
                #ignore comments
                if row[0][0] != '#':
                    r = []
                    for item in row:
                        r.append(item)
                    out.append(r)
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    return out

data = data_set(dataPath, subject_pattern)
ref = read_datafile(dataPath+reference)
operations = read_subfile(dataPath+subtractions)

poss_sheet = [[[], ['N-N=N'], ['blank', []]],
 [['N-N=N'], ['N-0=0'], []],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'], []],
 [[],
  ['blank',
   ['pt-gd=?'],
   ['gd-pt', 'pt-gd=gd', '0-N=N'],
   ['pt-gd=0', 'pt-gd=pt', '0-N=0']],
  ['blank', ['N-N=N'], []],
  ['blank', []]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', '0-N=0', 'gd-pt', 'pt-gd=gd', '0-N=N'],
  []],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['blank', []],
  ['blank', []]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'], [], []],
 [['N-0=0'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank', ['pt-gd=?'], ['pt-gd=pt'], ['gd-pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['pt-gd=?', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd', 'pt-gd=0'],
  []],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd', 'pt-gd=0'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd', 'pt-gd=0'],
  ['blank', ['pt-gd=?'], ['pt-gd=pt'], ['gd-pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'],
  ['N-N=N'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd', 'pt-gd=0'],
  []],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'], ['N-N=N'], []],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['N-N=N'],
  [],
  ['blank', ['pt-gd=?'], ['gd-pt', 'pt-gd=pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank', ['pt-gd=?'], ['pt-gd=pt'], ['gd-pt'], ['pt-gd=gd']]],
 [['N-0=0'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  []],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['N-0=0'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank', ['pt-gd=?'], ['gd-pt'], ['pt-gd=pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'], [], []],
 [[],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank',
   ['pt-gd=?'],
   ['gd-pt', 'pt-gd=gd', '0-N=N'],
   ['pt-gd=0', 'pt-gd=pt', '0-N=0']],
  ['blank', ['pt-gd=?'], ['gd-pt', 'pt-gd=pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'gd-pt', 'pt-gd=pt', 'pt-gd=gd'],
  ['N-N=N'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank',
   ['pt-gd=?'],
   ['gd-pt', 'pt-gd=gd', '0-N=N'],
   ['pt-gd=0', 'pt-gd=pt', '0-N=0']],
  ['blank', ['pt-gd=?'], ['gd-pt', 'pt-gd=pt'], ['pt-gd=gd']]],
 [['pt-gd=?', 'pt-gd=0', 'pt-gd=pt', 'gd-pt', 'pt-gd=gd'],
  ['pt-gd=?', 'gd-pt', 'pt-gd=gd', '0-N=N', 'pt-gd=0', 'pt-gd=pt', '0-N=0'],
  ['blank',
   ['pt-gd=?'],
   ['gd-pt', 'pt-gd=gd', '0-N=N'],
   ['pt-gd=0', 'pt-gd=pt', '0-N=0']],
  ['blank', []]]]
