#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, os, re, pickle

def read_datafile(filename, path):
    '''Return content from datafile of subject'''
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=' ')
        nb_ope = 0
        nb_col = 0
        content = {'results' : [], 'time' : 0, 'sheet' : [],
        'operations' : [] }
        rows = []
        try:
            for row in reader :
                rows.append(row)
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        for row in rows :
            #support empty lines
            if len(row) != 0 :
                #ignore comments
                if row[0][0] != '#':
                    if row[0] == 'time' :
                        content[row[0]] = int(row[1])
                    elif row[0] == 'sheet' :
                        for i, item in enumerate(row) :
                            if i != 0 :
                                content[row[0]].append(item)
                                #TODO share memory by linking instead of creating ope
                                ope = read_operations(os.path.join(path,item))
                                content['operations'].append(ope)
                    elif row[0] == 'judge' :
                        content.update({'judge' : row[1]})
                    else :
                        r = []
                        for item in row:
                            r.append(item)
                        if len(r) > 0 :
                            content['results'].append(r[0])
                            nb_ope += 1
                            nb_col += len(r[0])
        content.update({'nb_ope' : nb_ope})
        content.update({'nb_col' : nb_col})
    return content

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
        content = read_datafile(p, path)
        #keep only non empty datafiles
        if len(content['results']) > 0 :
            sub_data = {'path' : p}
            sub_data.update(content)
            data.append(sub_data)
        else :
            print(p, "is empty !")
    return data

def read_operations(filename):
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

def read_precomputations(path) :
    files = []
    for dirPath,dirNames,filName in os.walk(path):
        for theFile in filName:
            files.append(os.path.join(dirPath,theFile))
    files = sorted(files)
    sheets = {}
    for file_name in files :
        f = open(file_name, 'r')
        #keep name only (without .pickle extension and path)
        name = file_name[len(path):-7]
        sheets.update({name : pickle.load(f)})
    return sheets

def load_data(dataPath, subject_pattern) :
    #HACK to inform of wrong datafiles
    try :
        data = data_set(dataPath, subject_pattern)
        return data
    except :
        print "Unexpected error:", sys.exc_info()[0]
        raise
