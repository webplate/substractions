#!/usr/bin/env python
# -*- coding: utf-8 -*-


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

def bugId_perDigit(d1, d2, result):
    '''Returns the bug identifiers corresponding to the subtraction:
    (d1 - d2 = result)
    d1 and d2 must be integers, result can be integer or string,
    d1,d2 and result should be of length 1
    '''
    try :
        r = int(result)
    except ValueError :
        r = result
    bugs = []
    if d1 - d2 == r :      #no error at column level
        return bugs
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
    if d1 - d2 != r and len(bugs) == 0 :       #si l'erreur n'est pas prévue
        bugs.append('unexplained')
    return bugs

def bugId(n1, n2, result):
    '''Returns bugs found in subtraction:
        n1
       -n2
       ---
    result

    result must be string
    '''
    #~ bugs = []
    bugs_desc = [{'type':'subtraction', 'o1':n1, 'o2':n2, 'result':result}]
    correct = str(int(n1) - int(n2))
    cresult = clean_rslt(result)
    if cresult != correct :     #look for bugs only if erroneous result
        max_col = max(len(n1),len(n2),len(result))  #how many colons in the subtraction ?
        min_col = min(len(n1),len(n2),len(result))
        result = completeX(max_col, result)
        i = 0
        while i < max_col :
            pos = -i-1              #explore numbers from right to left (align to right)
            if i < len(n1):            #if result is not longer than operands
                d1 = int(n1[pos])
                if i < min_col :            #focus on completed columns
                    #check for incomplete subs : look only for erroneous
                    #columns if they're not from incomplete mental subtraction
                    #for this consider also digit from next column
                    n1_2 = n1[pos-1:len(n1)+pos+1]
                    n2_2 = n2[pos-1:len(n2)+pos+1]
                    result2 = cresult[pos-1:len(cresult)+pos+1]
                    #first operand must be on two columns
                    if (len(n1_2) == 2 and canBeInteger(result2)
                        #check for incomplete sub
                        and int(result2) == int(n1_2) - int(n2_2)
                        and int(result2) - int(n1_2) <= mental_limit):
                            #~ bugs.append(['incomplete'])
                            #and skip next column
                            #~ bugs.append(['incomplete'])
                            i += 1
                            bugs_desc.append({'pos':pos, 'type':'incomplete',
                            'o1':n1_2, 'o2':n2_2, 'result':result2})
                    else :
                        #check for unicolumn bug
                        d2 = int(n2[pos])
                        #look for bug in single column "pos"
                        bug_type = bugId_perDigit(d1, d2, result[pos])
                        #~ bugs.append(bug_type)
                        bugs_desc.append({'pos':pos, 'type':bug_type,
                            'o1':d1, 'o2':d2, 'result':result[pos]})
                else :        #then search for 'blank' bugs
                    d2 = int(n2[-min_col])
                    bug = bugId_perDigit(d1, d2, result[pos])
                    if bug != ['unexplained'] :         #spot 'blank' bug only if interesting
                        #~ bugs.append(['blank', bug])           #/!\blank bug associé avec d'autres bugs /!\
                        bugs_desc.append({'pos':pos, 'type':['blank', bug],
                            'o1':d1, 'o2':d2, 'result':result[pos]})
                    else :
                        #~ bugs.append(bug)
                        bugs_desc.append({'pos':pos, 'type':bug,
                            'o1':d1, 'o2':d2, 'result':result[pos]})
            else :
                #~ bugs.append(['over'])           #subject has written too many digits
                bugs_desc.append({'pos':pos, 'type':'over',
                    'result':result[pos]})
            #process next column
            i += 1
    else :
        #~ bugs.append(['correct'])        #subject is correct (operation level)
        bugs_desc.append({'type':'correct', 'o1':n1, 'o2':n2, 'result':result})
    #~ print n1,n2,result,bugs
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
    #list of independent empty lists
    #~ poss_bugs = [ [] for i in range(max_col)]
    poss_bugs = []
    while len(result) <= max_col :
        #~ print poss_bugs, max_col, result
        grp_bugs = bugId(n1, n2, result)
        #~ print grp_bugs
        for bug in grp_bugs :
            if 'pos' in bug :
                add = True
                #not interested by correct column sub or unexplained production
                if bug['type'] in ([], ['unexplained']) :
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

def dominancy(found, possible):
    '''Returns a dominancy score for found bugs
    '''
    print len(found[0]), len(possible[0])
    print found[0]
    print possible[0]
    #keep only list representation of bugs
    #~ found = [found[i][0] for i in range(len(found))]
    for op_bugs in possible :
        for col_bug in op_bugs :
            if col_bug in possible :
                #~ print col_bug
                pass


#~ count_correct(data, ref)
#~ print len(data)

#~ print bugId_perDigit(9,2,7)
#~ 
#~ print bugId('1813','215','1598'), 'correct'
#~ print bugId('1813','215','1600'), 'pt-gd=0'
#~ print bugId('1813','215','1700'), 'unexplained'
#~ print bugId('1813','215','170X')
#~ print bugId('1813','215',''), 'empty result'
#~ print bugId('1813','215','070X'), 'test not full col'
#~ print bugId('647', '45', '706')
#~ print bugId('1813','215','11598'), 'over'
#~ print bugId('1813','215','001598'), 'zero on left'
#~ print bugId('562','3','259'), 'incomplete sub : should only see blank bug as 62 - 3 = 59'
#~ print bugId('562','24','542'), 'incomplete sub (56-2=54)'
#~ print bugId('885','205','600'), 'should not show incomplete, should be length 3'
#~ print bugId('8888','11','8700'), 'incomplete and blank'


#~ for subject in data:
    #~ for i, result in enumerate(subject['results']):
        #~ print bugId(operations[i][0], operations[i][1], result)

#~ for i, result in enumerate(data[0]['results']):
    #~ print operations[i][0], operations[i][1], result
    #~ print bugId(operations[i][0], operations[i][1], result)


#~ print possible_bugs('647','45')
#~ out = possible_sheet(operations)

found = subject_sheet_bugs(data[0]['results'], operations)

dom = dominancy(found, poss_sheet)
