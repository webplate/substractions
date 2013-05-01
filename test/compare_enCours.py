#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_data import *

def count_correct(data, ref):
    for subject in data :
        nb_correct = 0
        for i,result in enumerate(subject['results']):
            if result == ref[i]:
                nb_correct += 1
        print subject['path'], nb_correct

def bugId_perDigit(d1, d2, result):
    '''Returns the bug identifiers corresponding to the substraction:
    (d1 - d2 = result)
    d1 and d2 must be integers, result can be integer or string
    '''
    bugs = []
    if d1 - d2 == result :      #no error
        return bugs
    if d1 < d2 :
        if d2 - d1 == result :  #inversion grand - petit
            bugs.append('pt-gd')
        if result == 0 :        #pt - gd = 0
            bugs.append('pt-gd=0')
        if result == 'X' :
            bugs.append('pt-gd=?')
        if result == d1 :
            bugs.append('pt-gd=pt')
        if result == d2 :
            bugs.append('pt-gd=gd')
    if result == 0 :
        if d1 == 0 :
            bugs.append('0-N=0')
        if d2 == 0 :
            bugs.append('N-0=0')
    if result == d2 :
        if d1 == 0 :
            bugs.append('0-N=N')
        if d2 == d1 :
            bugs.append('N-N=N')
    if d1 - d2 != result and len(bugs) == 0 :       #si l'erreur n'est pas prévue
        bugs.append('unexplained')
    return bugs

def bugId(n1, n2, result):
    '''Returns bugs found in substraction:
        n1
       -n2
       ---
    result
    
    '''
    bugs = []
    correct = str(int(n1) - int(n2))
    #how many colons in the substraction ?
    max_col = max(len(n1),len(n2),len(result))
    min_col = min(len(n1),len(n2),len(result))
    for i in range(max_col):
        pos = -i-1              #explore numbers from right to left (align to right)
        try :
            r = int(result[pos])
        except ValueError :
            r = result[pos]
        print pos, len(correct)
        if pos < -len(correct) :        #support longer subject result than correct result
            lpos = -len(correct)
        else :
            lpos = pos
        #test if subject is wrong to search for bugs...
        if r != int(correct[pos]) :
            d1 = int(n1[pos])
            if i < min_col :            #focus on completed columns
                d2 = int(n2[pos])
                bugs.append(bugId_perDigit(d1, d2, r))
            else :        #search for 'blank' bug
                d2 = int(n2[-min_col])
                bug = bugId_perDigit(d1, d2, r)
                if bug != ['unexplained'] :
                    bugs.append(['blank', bug])           #/!\blank bug associé avec d'autres bugs /!\
                else :
                    bugs.append(bug)
        else :
            bugs.append([])
    return n1, n2, result, bugs

def find_dominant():
    ''''''

#~ count_correct(data, ref)
#~ print len(data)

#~ print bugId_perDigit(9,2,7)

#~ print bugId('1813','215','1598'), 'correct'
#~ print bugId('1813','215','1600'), 'pt-gd=0'
#~ print bugId('1813','215','1700'), 'unexplained'
#~ print bugId('1813','215','170X')
#~ print bugId('1813','215','070X'), 'test not full col'
#~ print bugId('647', '45', '706')

for subject in data:
    for i, result in enumerate(subject['results']):
        print operations[i][0], operations[i][1], result
        print bugId(operations[i][0], operations[i][1], result)
