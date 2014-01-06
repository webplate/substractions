#!/usr/bin/env python
# -*- coding: utf-8 -*-

import read_data as r_d
import transform_data as t_d
import parameters

import pickle
import pprint

def count_correct(data, ref):
    for subject in data :
        nb_correct = 0
        for i,result in enumerate(subject['results']):
            if result == ref[i]:
                nb_correct += 1
        print subject['path'], nb_correct

def correct_result(operands, o_type='subtraction') :
    '''returns the correct result for an operation on two str operands'''
    if o_type == 'subtraction' :
        result = int(operands[0]) - int(operands[1])
        return str(result)

def bugId_perDigit(d1, d2, r) :
    '''Returns the bug identifiers corresponding to the subtraction:
    (d1 - d2 = r)
    parameters must be strings,
    d1,d2 and r should be of length 1
    '''
    bugs = []
    if t_d.canBeInteger(r) and t_d.canBeInteger(d1) and t_d.canBeInteger(d2) :
        r = int(r)
        d1 = int(d1)
        d2 = int(d2)
        if d1 - d2 == r :      #no error at column level
            return ['correct_col']
        if d1 < d2 and d1 != 0 :
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
        #~ elif d1 < d2 and d1 == 0 :
            #~ if d2 - d1 == r :  #inversion grand - petit
                #~ bugs.append('gd-ptZ')
            #~ if r == 0 :        #pt - gd = 0
                #~ bugs.append('pt-gd=0Z')
            #~ if r == 'X' :
                #~ bugs.append('pt-gd=?Z')
            #~ if r == d1 :
                #~ bugs.append('pt-gd=ptZ')
            #~ if r == d2 :
                #~ bugs.append('pt-gd=gdZ')
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
    #n2_2 can be of length one for incomplete sub
    if len(n2_2) > 1 and n2_2[0] == 'X' :
        n2_2 = n2_2[1]
    #first operand must be on two columns
    if (len(n1_2) > 1 and t_d.canBeInteger(result2)
        and t_d.canBeInteger(n2_2) and t_d.canBeInteger(n1_2)
        #check for incomplete sub
        and int(result2) == int(n1_2) - int(n2_2)
        and int(result2) - int(n1_2) <= parameters.mental_limit):
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
    cresult = t_d.clean_rslt(result)
    if cresult != correct :     #look for bugs only if erroneous result
        max_col = max(len(n1),len(n2),len(result))  #how many colons in the subtraction ?
        max_oper = max(len(n1),len(n2))
        min_col = min(len(n1),len(n2),len(result))
        result = t_d.completeX(max_col, result)
        n1 = t_d.completeX(max_col, n1)
        n2 = t_d.completeX(max_col, n2)
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
                #look for bug in single column "pos"
                bug_types = bugId_perDigit(d1, d2, result[pos])
                #there could be a blank bug
                if d2 == 'X' and bug_types != ['copy'] :
                    d2_shifted = n2[-min_col]
                    bug_types_s = bugId_perDigit(d1, d2_shifted, result[pos])
                    if bug_types_s != ['unexplained'] :         #spot 'blank' bug only if interesting
                        for bt in bug_types_s :
                            bugs_desc.append({'pos':pos, 'type':'blank_'+bt,
                            'o1':d1, 'o2':d2_shifted, 'result':result[pos]})
                            explained_pos.append(pos)
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
    result = t_d.completeX(max_col, '')
    poss_bugs = []
    while len(result) <= max_col :
        grp_bugs = bugId(n1, n2, result)
        for bug in grp_bugs :
            if 'pos' in bug :
                add = True
                #not interested by unexplained production
                if bug['type'] == 'unexplained' :
                    add = False
                #keep only different bugs on a same position
                for pbug in poss_bugs :
                    if (bug['pos'] ==  pbug['pos']
                    and bug['type'] == pbug['type']):
                        add = False
                if add:
                    poss_bugs.append({'pos':bug['pos'],
                    'type':bug['type'], 'result':bug['result']})

        r += 1
        result = t_d.completeX(max_col, str(r))
    return poss_bugs

def possible_sheet(sheet, silent=True) :
    '''Give possible bugs for all subtractions in sheet
    '''
    p_s = []
    for n1, n2 in sheet :
        if silent == False :
            print 'Precomputing for ', (n1, n2)
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

            t = col_bug['type']
            #there is a congruent bug
            if (col_bug['type'] not in ('correct_col', 'copy')
            and col_bug['type'] in in_place) :
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

def profile(scores) :
    '''create bug profile of subject
    returns list of (dominancy, bug) couples
    '''
    bugs_tuples = []
    for bug in scores :
        nb_sub, nb_poss = scores[bug]
        proportion = float(nb_sub)/nb_poss
        bugs_tuples.append((proportion, bug))
    bugs_tuples = sorted(bugs_tuples, reverse=True,
    key=lambda strategy: strategy[0])   # sort by proportion
    return bugs_tuples


def simulate(dom_bugs, poss_sheet, operations, subject_id) :
    '''gives a result sheet congruent with the dominant_bugs
    '''
    simul = [ [] for i in range(len(poss_sheet)) ]
    results = []
    dom_bugs_names = [tupl[1] for tupl in dom_bugs]
    for index, subtraction in enumerate(poss_sheet) :
        #select possible productions for a sub
        for bug in subtraction :
            #select dominancy relative to the bug type in question
            for (dom, name) in dom_bugs :   #for candidate
                if name == bug['type'] :
                    dominancy = dom
                    bug.update({'dominancy':dominancy})
            gen_pos = [ bug2['pos'] for bug2 in simul[index] ]
            if bug['type'] in dom_bugs_names :
                if bug['pos'] not in gen_pos : #new bug
                    simul[index].append(bug)
                else :   #competition between bugs (keep most dominant)
                    for bug3 in simul[index] :    #for current
                        if (bug3['pos'] == bug['pos']
                        and dominancy > bug3['dominancy']) :
                            simul[index].append(bug)
                            simul[index].remove(bug3)
            elif (bug['type'] in ('correct_col', 'copy')
            and bug['pos'] not in gen_pos) :    #basic strategies (if no dominant bug suitable)
                bug.update({'dominancy':0})
                simul[index].append(bug)

#check selected bugs to have a complete result...todo
        #build the corresponding result
        positions = [ bug['pos'] for bug in simul[index] ]
        result_lst = [ '?' for i in range(-min(positions)) ]
        for bug in simul[index] :
            if len(bug['result']) == 1 :
                result_lst[bug['pos']] = bug['result']
            elif len(bug['result']) == 2 :
                result_lst[bug['pos']] = bug['result'][1]
                result_lst[bug['pos']-1] = bug['result'][0]
        result = ''
        for c in result_lst :
            if c == '?' : #WARNING if empty simulation
                print 'Empty simulation for : ', subject_id, operations[index]
            result = result + c
        results.append(result)
    return simul, results

def serialize(subject, poss_sheets) :
    """Concatenate if necessary productions from multiple protocols/exercises
    and concatenate associated possibilities"""
    #concatenate operations
    operations = []
    for ope in subject['operations'] :
        operations.extend(ope)
    #concatenate precomputed possibilities
    poss_sheet = []
    for sheet in subject['sheet'] :
        poss_sheet.extend(poss_sheets[sheet])
    #check len of subject production vs len of exercise
    if len(operations) != len(subject['results']) :
        print 'WARNING : incongruency between subject datafile and protocols for ', subject['path']
    return operations, poss_sheet

def write_precomputations(sheet, file_name) :
    f = open(file_name, 'w')
    p_s = possible_sheet(sheet, silent=False)
    pprint.pprint(p_s)
    pickle.dump(p_s, f)

#TEST SUITE :
#~ print bugId_perDigit(2,9,0)
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

#~ data, ref, operations = r_d.load_data(parameters.dataPath,parameters.subject_pattern,parameters.reference,parameters.subtractions)

#~ #recompute the possible bugs of the sheet
#~ write_precomputations(operations, parameters.precomputation_file)

#~ found = subject_sheet_bugs(data[parameters.default_sub]['results'], operations)
#~ pprint.pprint(operations)
#compute dominancies of subject
#~ poss_sheet = read_precomputations(parameters.precomputation_file)
#~ scores = dominancy(found, poss_sheet)
#create profile of subject (most dominant bugs)
#~ dom_bugs = profile(scores, parameters.dominancy_thre)
#compute simulation according to profile
#~ simul_sheet = simulate(dom_bugs, poss_sheet)
#~ pprint.pprint(simul_sheet[1])
