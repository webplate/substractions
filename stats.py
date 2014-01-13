#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  
#  Copyright 2013 z <z@z-1005PE>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import operator
import numpy as np

import bugs


def subject_congruency(subject_id, data, poss_sheet, simul_sheet, operations, sheet_id) :
    '''gives nb of congruencies between subject production and simulation
    at column and operation level
    '''
    #~ print len(simul_sheet), len(operations)
    nb_correct_ope, nb_ope, nb_correct_col, nb_col = (0, 0, 0, 0)
    #+-1 tolerance TODO at operation level
    #check congruency between simul result and subject data
    for j, sim_result in enumerate(simul_sheet) :
        #offset for half ope simulations
        if bugs.parameters.randomize and sheet_id == 0 :
            j += 20
        #exclude empty answers from valid answers
        #and exclude correctly answered operations
        c_result = bugs.correct_result(operations[j])
        if (sim_result == data[subject_id]['results'][j] and
        not data[subject_id]['results'][j] == c_result):
            nb_correct_ope += 1
        if (data[subject_id]['results'][j] not in ['X','G'] and
        not data[subject_id]['results'][j] == c_result) :
            nb_ope += 1
            #check at column level (last nb first)
            pos = -1
            len_sub = len(data[subject_id]['results'][j])
            min_len = min(len_sub, len(sim_result))
            for k in range(len_sub) :
                if -pos <= min_len :
                    if bugs.parameters.tolerant and bugs.t_d.canBeInteger(sim_result[pos]) :
                        tol_values = (str(int(sim_result[pos])+1), sim_result[pos],
                    str(int(sim_result[pos])-1))
                    else :
                        tol_values = [sim_result[pos]]
                    #compare with eventual +-1 tolerance
                    if data[subject_id]['results'][j][pos] in tol_values :
                        nb_correct_col += 1

                    #exclude empty answers from valid answers
                    if data[subject_id]['results'][j][pos] not in ['X','G'] :
                        nb_col += 1
                #for columns where subject answers and no sim is made
                else :
                    #exclude empty answers from valid answers
                    if data[subject_id]['results'][j][pos] not in ['X','G'] :
                        nb_col += 1
                pos -= 1
    return nb_correct_ope, nb_ope, nb_correct_col, nb_col

def profile(subject, operations, results, poss_sheet, profile_size, repartition) :
    #create profile of subject (ordered by dominancy list of (dom, bug) )
    found_bugs = bugs.subject_sheet_bugs(results, operations)
    scores = bugs.dominancy(found_bugs, poss_sheet)
    subject.update({'scores' : scores})
    dom_bugs_l = bugs.profile(scores)
    subject.update({'profile' : dom_bugs_l})
    #populate repartition of bugs between subjects
    for dom, bug_type in dom_bugs_l :
        for threshold in bugs.parameters.dom_thre :
            if bug_type in repartition[threshold] :
                if dom > threshold :
                    repartition[threshold][bug_type] += 1
            else :
                if dom > threshold :
                    repartition[threshold].update({bug_type : 1})
                else :
                    repartition[threshold].update({bug_type : 0})
                
    #a truncated version for cognitive plausability
    #(used for ordered profiles and simulation)
    dom_bugs = dom_bugs_l[:profile_size]
    subject.update({'short_profile' : dom_bugs})
    ordered_prof = [dom_bug[1] for dom_bug in dom_bugs]
    subject.update({'ord_profile' : ordered_prof})
    return dom_bugs

def simulate(subject, possible_sheet, operations) :
    #compute simulation according to profile
    simul_sheet = bugs.simulate(subject['short_profile'],
    possible_sheet, operations, subject['id'])
    subject.update({'sim_rslt' : simul_sheet[1]})
    subject.update({'sim_dtl' : simul_sheet[0]})

def evaluate(subject, data, operations, poss_sheet, 
all_cong, all_sc, ls_ord_prof) :
    #evaluate simulation over some results
    scores = subject_congruency(subject['id'], data, poss_sheet,
    subject['sim_rslt'], operations, subject['sim_sheet'])
    subject.update({'score_ope' : (scores[0], scores[1])})
    subject.update({'score_col' : (scores[2], scores[3])})
    subject.update({'perf_ope' : float(scores[0])/scores[1]})
    subject.update({'perf_col' : float(scores[2])/scores[3]})
    #compute global dominancies
    bug_scores = subject['scores']
    if all_sc == {} :
        all_sc.update(bug_scores)
    else:
        for key in bug_scores :
            all_sc[key] = (bug_scores[key][0]+all_sc[key][0],
            bug_scores[key][1]+all_sc[key][1])
    #compute global congruency
    for i in range(4) :
        all_cong[i] += scores[i]
    #find dict to update for a supplementary occurence of ordered profile
    dico = [prof for prof in ls_ord_prof if prof['profile'] == subject['ord_profile']]
    if len(dico) == 0 : #this profile has never occured yet
        ls_ord_prof.append({'profile' : subject['ord_profile'], 'occ' : 1})
    else : #no duplicates
        dico = dico[0]
        dico.update({'occ' : dico['occ']+1})

def analysis(data, poss_sheets, profile_size) :
    '''Precompute stats on whole dataset, add result per subject in data
    returns stats on whole set
    '''
    all_cong = [0, 0, 0, 0] #congruency at global level
    all_sc = {} #dominancy scores at global level
    ls_ord_prof = [] #list of ordered profiles globally
    repartition = {} 
    for threshold in bugs.parameters.dom_thre :
        repartition.update({threshold : {}})
    #profile, simulate, evaluate
    for subject_id in range(len(data)) :
        subject = data[subject_id]
        if bugs.parameters.randomize :
            #role a dice to avoid effect order between sheets 
            #create intervals : one for profile and one for sim
            if float(np.random.random(1)) > 0.5 :
                subject.update({'sim_sheet' : 0})
                prof_i = range(20)
                sim_i = range(20, 40)
            else :
                subject.update({'sim_sheet' : 1})
                prof_i = range(20, 40)
                sim_i = range(20)
        else :
            #no different subsets
            prof_i = range(20)
            sim_i = prof_i
            subject.update({'sim_sheet' : 0})
        operations, poss_sheet = bugs.serialize(subject, poss_sheets)
        #subset of ope and results for profiling
        prof_ope = [operations[i] for i in prof_i]
        prof_res = [subject['results'][i] for i in prof_i]
        prof_poss = [poss_sheet[i] for i in prof_i]
        #create profile of subject (ordered by dominancy list of (dom, bug) )
        profile(subject, prof_ope, prof_res, prof_poss, profile_size,
        repartition)
        #subset of ope and results for simulation
        sim_ope = [operations[i] for i in sim_i]
        sim_poss = [poss_sheet[i] for i in sim_i]
        #compute simulation according to profile
        simulate(subject, sim_poss, sim_ope)
        #evaluate
        evaluate(subject, data, operations, sim_poss,
        all_cong, all_sc, ls_ord_prof)
    #Ordinate bugs along a criteria
    chronology = operator.itemgetter('occ')
    ls_ord_prof.sort(key=chronology)
    global_stats = {'ord_profile' : ls_ord_prof,
    'scores' : all_sc,
    'score_ope' : (all_cong[0], all_cong[1]),
    'score_col' : (all_cong[2], all_cong[3]),
    'perf_ope' : float(all_cong[0])/all_cong[1],
    'perf_col' : float(all_cong[2])/all_cong[3],
    'repartition' : repartition,
    'nb_subjects' : len(data)}
    return global_stats

def give_percent(scores) :
    nb_correct_ope, nb_ope, nb_correct_col, nb_col = scores
    correct_ope = nb_correct_ope / float(nb_ope)
    correct_col = nb_correct_col / float(nb_col)
    percents = ["Perf at operation level : {0:.0%}".format(correct_ope), "Perf at column level : {0:.0%}".format(correct_col)]
    return percents
