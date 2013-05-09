#!/usr/bin/env python
# -*- coding: utf-8 -*-


from read_data import *
from transform_data import *

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
    d1 and d2 must be integers, result can be integer or string
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
    bugs = []
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
                    d2 = int(n2[pos])
                    #check for incomplete subs : look only for erroneous
                    #columns if they're not from incomplete mental subtraction
                    #for this consider also digit from next column
                    correct2 = correct[pos-1:len(correct)+pos+1]
                    n1_2 = n1[pos-1:len(n1)+pos+1]
                    n2_2 = n2[pos-1:len(n2)+pos+1]
                    result2 = cresult[pos-1:len(cresult)+pos+1]
                    try :
                        r2 = int(result2)
                    except ValueError :
                        check_incomplete = False
                    else :
                        check_incomplete = (r2 == int(n1_2) - int(n2_2)
                            and r2 - int(n1_2) <= mental_limit)
                    if check_incomplete :
                        bugs.append(['incomplete'])
                        #and skip next column
                        bugs.append(['incomplete'])
                        i += 1
                    else :
                        bugs.append(bugId_perDigit(d1, d2, result[pos]))
                else :        #then search for 'blank' bugs
                    d2 = int(n2[-min_col])
                    bug = bugId_perDigit(d1, d2, result[pos])
                    if bug != ['unexplained'] :         #spot 'blank' bug only if interesting
                        bugs.append(['blank', bug])           #/!\blank bug associé avec d'autres bugs /!\
                    else :
                        bugs.append(bug)
            else :
                bugs.append(['over'])           #subject has written too many digits
            #process next column
            i += 1
    else :
        bugs.append(['correct'])        #subject is correct (operation level)
    #~ print n1,n2,result,bugs
    return bugs

def possible_bugs(n1, n2) :
    '''give potential bugs for a subtraction
    '''
    max_col = max(len(n1),len(n2))
    #start at -1 (corresponding to 'X' : empty response)
    r = -1
    result = completeX(max_col, '')
    #list of independent empty lists
    poss_bugs = [ [] for i in range(max_col) ]
    while len(result) <= max_col :
        #~ print poss_bugs, max_col, result
        grp_bugs = bugId(n1, n2, result)
        for i, bugs in enumerate(grp_bugs) :
            #~ print i, bugs
            for bug in bugs :
                if (bug not in poss_bugs[i]
                and bug != 'correct'
                and bug != 'unexplained') :
                    #~ print result
                    poss_bugs[i].append(bug)
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

def find_dominant(found, possible):
    '''Returns "dominant bugs" in subject results (found) according to
    possible bugs (possible)

    NOT YET !!
    '''
    score = 0
    for i, op_bugs in enumerate(found) :
        for col_bug in possible[i] :
            if col_bug in op_bugs :
                print op_bugs, col_bug
                score += 1
    print score
    return score

def dominancy(found, possible):
    '''Returns a dominancy score for found bugs
    '''
    pass

#~ count_correct(data, ref)
#~ print len(data)

#~ print bugId_perDigit(9,2,7)
#~ 
print bugId('1813','215','1598'), 'correct'
print bugId('1813','215','1600'), 'pt-gd=0'
print bugId('1813','215','1700'), 'unexplained'
print bugId('1813','215','170X')
print bugId('1813','215','070X'), 'test not full col'
print bugId('647', '45', '706')
print bugId('1813','215','11598'), 'over'
print bugId('1813','215','001598'), 'zero on left'
print bugId('562','3','259'), 'incomplete sub : should only see blank bug as 62 - 3 = 59'
print bugId('562','24','542'), 'incomplete sub (56-2=54)'


#~ for subject in data:
    #~ for i, result in enumerate(subject['results']):
        #~ print bugId(operations[i][0], operations[i][1], result)

#~ for i, result in enumerate(data[0]['results']):
    #~ print operations[i][0], operations[i][1], result
    #~ print bugId(operations[i][0], operations[i][1], result)

#~ print possible_bugs('83','44')
#~ out= possible_sheet([('647','45'),('885','205')])

#~ out = possible_sheet(operations)

#~ found = subject_sheet_bugs(data[0]['results'], operations)
#~ dom = find_dominant(found, poss_sheet)
