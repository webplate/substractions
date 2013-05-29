#!/usr/bin/env python
# -*- coding: utf-8 -*-

def completeX(length, string):
    '''adds necessary 'X's before string so that len(string)==length
    '''
    l = len(string)
    if length > l :
        d = length - l
        n = 'X'*d + string
    else :
        n = string
    return n

def clean_rslt(string):
    '''remove preceeding zeros
    '''
    nb_zeros = 0
    for i in range(len(string)) :
        if string[i] == '0' :
            nb_zeros += 1
        else :
            break
    return string[nb_zeros:]

def flatten(l):
    for el in l:
        if isinstance(el, list) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def canBeInteger(string):
    try:
        integer = int(string)
    except ValueError :
        return False
    else :
        return True

def format_bug_desc(dic):
    lst = []
    lst.append(str(dic['o1'])+'-'+str(dic['o2'])+'='+str(dic['result']))
    lst.append(str(dic['type']))
    return lst
