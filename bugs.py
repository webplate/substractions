#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
from read_data import *
from transform_data import *
from precomputed import poss_sheet

def count_correct(data, ref):
    for subject in data :
        nb_correct = 0
        for i,result in enumerate(subject['results']):
            if result == ref[i]:
                nb_correct += 1
        print subject['path'], nb_correct

def bugId_perDigit(d1, d2, r):
    '''Returns the bug identifiers corresponding to the subtraction:
    (d1 - d2 = r)
    parameters must be strings,
    d1,d2 and r should be of length 1
    '''
    #~ print d1, d2, result
    bugs = []
    if canBeInteger(r) and canBeInteger(d1) and canBeInteger(d2) :
        r = int(r)
        d1 = int(d1)
        d2 = int(d2)
        if d1 - d2 == r :      #no error at column level
            return ['correct_col']
        if d1 < d2 :
            if d2 - d1 == r :  #inversion grand - petit
                bugs.append('gd-pt')
            if r == 0 :        #pt - gd = 0
                bugs.append('pt-gd=0')
            if r == 'X' :
                bugs.append('pt-gd=?')
            if r == d1 :
                bugs.append('pt-gd=pt')
            if r == d2 :
                bugs.append('pt-gd=gd')
        if r == 0 :
            if d1 == 0 :
                bugs.append('0-N=0')
            if d2 == 0 :
                bugs.append('N-0=0')
        if r == d2 :
            if d1 == 0 :
                bugs.append('0-N=N')
            if d2 == d1 :
                bugs.append('N-N=N')
    if r == d1 and d2 == 'X' :           #recopiage de ligne sup vers résultat
        return ['copy']
    if len(bugs) == 0 :       #si l'erreur n'est pas prévue
        return ['unexplained']
    return bugs

def bugId_perDouble(n1, n2, result, pos):
    '''identify bugs on double columns
    returns bugs list and newly explained positions list
    '''
    bugs_desc = []
    explained_pos = []
    #check for incomplete subs : look only for erroneous
    #columns if they're not from incomplete mental subtraction
    #for this consider also digit from next column
    n1_2 = n1[pos-1:len(n1)+pos+1]
    n2_2 = n2[pos-1:len(n2)+pos+1]
    result2 = result[pos-1:len(result)+pos+1]
    #~ print n1_2, n2_2, result2
    #n2_2 can be of length one for incomplete sub
    if len(n2_2) > 1 and n2_2[0] == 'X' :
        n2_2 = n2_2[1]
    #first operand must be on two columns
    if (len(n1_2) > 1 and canBeInteger(result2)
        and canBeInteger(n2_2) and canBeInteger(n1_2)
        #check for incomplete sub
        and int(result2) == int(n1_2) - int(n2_2)
        and int(result2) - int(n1_2) <= mental_limit):
            bugs_desc.append({'pos':pos, 'type':'incomplete',
            'o1':n1_2, 'o2':n2_2, 'result':result2})
            explained_pos.append(pos)
            explained_pos.append(pos-1)
    return bugs_desc, explained_pos

def bugId(n1, n2, result):
    '''Returns bugs found in subtraction:
        n1
       -n2
       ---
    result

    result must be string
    '''
    bugs_desc = [{'type':'subtraction', 'o1':n1, 'o2':n2, 'result':result}]
    correct = str(int(n1) - int(n2))
    cresult = clean_rslt(result)
    if cresult != correct :     #look for bugs only if erroneous result
        max_col = max(len(n1),len(n2),len(result))  #how many colons in the subtraction ?
        max_oper = max(len(n1),len(n2))
        min_col = min(len(n1),len(n2),len(result))
        result = completeX(max_col, result)
        n1 = completeX(max_col, n1)
        n2 = completeX(max_col, n2)
        explained_pos = []
        i = 0
        while i < max_col :
            pos = -i-1              #explore numbers from right to left (align to right)
            if i < max_oper:            #if result is not longer than operands
                #check for double columns bugs (incomplete)
                b_d, e_p = bugId_perDouble(n1, n2, cresult, pos)
                bugs_desc.extend(b_d)
                explained_pos.extend(e_p)
                #check for unicolumn bug
                d1 = n1[pos]
                d2 = n2[pos]
                #there could be a blank bug
                if d2 == 'X' and bug_types != ['copy'] :
                    d2_shifted = n2[-min_col]
                    bug_types = bugId_perDigit(d1, d2_shifted, result[pos])
                    #~ print explained_pos, pos
                    if bug_types != ['unexplained'] :         #spot 'blank' bug only if interesting
                        for bt in bug_types :
                            bugs_desc.append({'pos':pos, 'type':['blank', bt],
                            'o1':d1, 'o2':d2_shifted, 'result':result[pos]})
                            explained_pos.append(pos)
                #look for bug in single column "pos"
                bug_types = bugId_perDigit(d1, d2, result[pos])
                #add unicolumn bugs
                for bt in bug_types :
                    #ignore unexplained bugs if they're explained otherwise
                    # = present in explained_pos
                    if not (pos in explained_pos and bt == 'unexplained') :
                        bugs_desc.append({'pos':pos, 'type':bt,
                        'o1':d1, 'o2':d2, 'result':result[pos]})
            else :
                #subject has written too many digits
                bugs_desc.append({'pos':pos, 'type':'over',
                    'result':result[pos]})
            #process next column
            i += 1
    else :
        #subject is correct (operation level)
        bugs_desc.append({'type':'correct', 'o1':n1, 'o2':n2, 'result':result})
    return bugs_desc

def possible_bugs(n1, n2) :
    '''give potential bugs for a subtraction
    n1 - n2
    parameters should be of string type
    '''
    max_col = max(len(n1),len(n2))
    #start at -1 (corresponding to 'X' : empty response)
    r = -1
    result = completeX(max_col, '')
    poss_bugs = []
    while len(result) <= max_col :
        grp_bugs = bugId(n1, n2, result)
        for bug in grp_bugs :
            if 'pos' in bug :
                add = True
                #not interested by unexplained production or correct column
                if bug['type'] in ('unexplained', 'correct_col', 'copy') :
                    add = False
                #keep only different bugs on a same position
                for pbug in poss_bugs :
                    if (bug['pos'] ==  pbug['pos']
                    and bug['type'] == pbug['type']):
                        add = False
                if add:
                    poss_bugs.append({'pos':bug['pos'], 'type':bug['type']})

        r += 1
        result = completeX(max_col, str(r))
    return poss_bugs

def possible_sheet(sheet) :
    '''Give possible bugs for all subtractions in sheet
    '''
    p_s = []
    for n1, n2 in sheet :
        p_s.append(possible_bugs(n1, n2))
    return p_s

def subject_sheet_bugs(subject_data, operations) :
    '''Gives detected bugs of subjects in sheet constituted by operations
    '''
    bugs = []
    for i, (n1, n2) in enumerate(operations) :
        bugs.append(bugId(n1, n2, subject_data[i]))
    return bugs

def dominancy(found, possible) :
    '''Returns a dominancy score for found bugs
    '''
    scores = {}
    for i, op_bugs in enumerate(possible) :
        fnd_bugs = found[i]
        for col_bug in op_bugs :
            #found bugs in the same position
            in_place = [fnd_bugs[j]['type']
            for j in range(len(fnd_bugs))
            if 'pos' in fnd_bugs[j]
            and fnd_bugs[j]['pos'] == col_bug['pos']]

            t = str(col_bug['type'])
            #there is a congruent bug
            if col_bug['type'] in in_place :
                #~ pprint.pprint(col_bug['type'])
                if t in scores :
                    nb_sub, nb_poss = scores[t]
                    new_score = (nb_sub+1, nb_poss+1)
                    scores.update({t:new_score})
                else :
                    scores.update({t:(0, 1)})
            #the subject didn't produce this possible bug
            else :
                if t in scores :
                    nb_sub, nb_poss = scores[t]
                    new_score = (nb_sub, nb_poss+1)
                    scores.update({t:new_score})
                else :
                    scores.update({t:(0, 1)})
    return scores


#~ print bugId_perDigit(2,9,0)

#TEST SUITE :
#~ pprint.pprint(bugId('1813','215','1598'))#, 'correct'
#~ pprint.pprint(bugId('1813','215','1600'))#, 'pt-gd=0'
#~ pprint.pprint(bugId('1813','215','1700'))#, 'unexplained'
#~ pprint.pprint(bugId('1813','215','170X'))#
#~ pprint.pprint(bugId('1813','215',''))#, 'empty result'
#~ pprint.pprint(bugId('1813','215','070X'))#, 'test not full col'
#~ pprint.pprint(bugId('647', '45', '706'))#
#~ pprint.pprint(bugId('1813','215','11598'))#, 'over'
#~ pprint.pprint(bugId('1813','215','001598'))#, 'zero on left'
#~ pprint.pprint(bugId('562','3','259'))#, 'incomplete sub : should only see blank bug as 62 - 3 = 59'
#~ pprint.pprint(bugId('562','24','542'))#, 'incomplete sub (56-2=54)'
#~ pprint.pprint(bugId('885','205','600'))#, 'should not show incomplete, should be length 3'
#~ pprint.pprint(bugId('8888','11','8700'))#, 'blank' (not incomplete)
#~ pprint.pprint(bugId('562','3','561'))#, copy of first line, should be correct and not unexplained
#~ pprint.pprint(bugId('102','39','137'))#, copy of first line, should be correct and not blank bug
#~ pprint.pprint(bugId('647','45','202'))#, blank bug and no correct_col (6-4=2) !

#~ for subject in data:
    #~ for i, result in enumerate(subject['results']):
        #~ print bugId(operations[i][0], operations[i][1], result)

#~ for i, result in enumerate(data[0]['results']):
    #~ print operations[i][0], operations[i][1], result
    #~ print bugId(operations[i][0], operations[i][1], result)


#~ pprint.pprint(possible_bugs('647','45'))
#~ pprint.pprint(possible_sheet(operations))

#~ found = subject_sheet_bugs(data[default_sub]['results'], operations)

#~ dom = dominancy(found, poss_sheet)
#~ pprint.pprint(dom)
