#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, os, re

def read_datafile(filename):
    '''Return content from datafile of subject'''
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        out = []
        try:
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
            if re.match(pattern, theFile) :
                files.append(os.path.join(dirPath,theFile))
    files = sorted(files)
    return files

def data_set(path, pattern):
    '''Returns a list of dictionnaries, one for each subject
    '''
    data = []
    files_p = list_files(path, pattern)
    for p in files_p :
        results = read_datafile(p)
        #keep only non empty datafiles
        if len(results) > 0 :
            data.append({'path' : p, 'results' : results})
        else :
            print(p, "is empty !")
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

def load_data(dataPath, subject_pattern, reference, subtractions) :
    #HACK to inform of wrong datafiles
    try:
        data = data_set(dataPath, subject_pattern)
        ref = read_datafile(dataPath+reference)
        operations = read_subfile(dataPath+subtractions)
        return data, ref, operations
    except:
        print "Wrong datapaths :"
        print dataPath+reference
        print dataPath+subtractions
        print "set these in parameters.py"
