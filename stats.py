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
import bugs

def subject_congruency(subject_id, data, poss_sheet, simul_sheet, operations) :
    '''gives nb of congruencies between subject production and simulation
    at column and operation level
    '''
    nb_correct_ope, nb_ope, nb_correct_col, nb_col = (0, 0, 0, 0)
    #+-1 tolerance TODO at operation level
    #check congruency between simul result and subject data
    for j, sim_result in enumerate(simul_sheet) :
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
                    #~ print sim_result[pos] , data[subject_id]['results'][j][pos], sim_result, data[subject_id]['results'][j],nb_correct_ope, nb_correct_col
                    if bugs.parameters.tolerant and bugs.t_d.canBeInteger(sim_result[pos]) :
                        tol_values = (str(int(sim_result[pos])+1), sim_result[pos],
                    str(int(sim_result[pos])-1))
                    else :
                        tol_values = [sim_result[pos]]
                    #compare with eventual +-1 tolerance
                    if data[subject_id]['results'][j][pos] in tol_values :
                        nb_correct_col += 1
                        #~ print sim_result[pos] , data[subject_id]['results'][j][pos], sim_result, data[subject_id]['results'][j],nb_correct_ope, nb_correct_col

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

def analysis(data, poss_sheets) :
    '''Precompute stats on whole dataset, add result per subject in data
    returns stats on whole set
    '''
    all_cong = [0, 0, 0, 0] #congruency at global level
    all_sc = {} #dominancy scores at global level
    ls_ord_prof = [] #list of ordered profiles globally
    for subject_id in range(len(data)) :
        subject = data[subject_id]
        operations, poss_sheet = bugs.serialize(subject, poss_sheets)
        #create profile of subject (ordered by dominancy list of (dom, bug) )
        found_bugs = bugs.subject_sheet_bugs(subject['results'], operations)
        scores = bugs.dominancy(found_bugs, poss_sheet)
        dom_bugs_l = bugs.profile(scores)
        subject.update({'profile' : dom_bugs_l})
        #compute global dominancies
        if all_sc == {} :
            all_sc = scores
        for key in scores :
            all_sc[key] = (scores[key][0]+all_sc[key][0],
            scores[key][1]+all_sc[key][1])
        #a truncated version for cognitive plausability
        #(used for ordered profiles and simulation)
        dom_bugs = dom_bugs_l[:bugs.parameters.profile_size]
        ordered_prof = [dom_bug[1] for dom_bug in dom_bugs]
        subject.update({'ord_profile' : ordered_prof})
        #compute simulation according to profile
        b_simul_sheet = bugs.simulate(dom_bugs, poss_sheet, operations, subject_id)[1]
        scores = subject_congruency(subject_id, data, poss_sheet, b_simul_sheet,
        operations)
        subject.update({'score_ope' : (scores[0], scores[1])})
        subject.update({'score_col' : (scores[2], scores[3])})
        subject.update({'perf_ope' : float(scores[0])/scores[1]})
        subject.update({'perf_col' : float(scores[2])/scores[3]})
        #compute global congruency
        for i in range(4) :
            all_cong[i] += scores[i]
        #find dict to update for a supplementary occurence of ordered profile
        dico = [prof for prof in ls_ord_prof if prof['profile'] == ordered_prof]
        if len(dico) == 0 : #this profile has never occured yet
            ls_ord_prof.append({'profile' : ordered_prof, 'occ' : 1})
        else : #no duplicates
            dico = dico[0]
            dico.update({'occ' : dico['occ']+1})
    #Ordinate subjects along a criteria
    chronology = operator.itemgetter('occ')
    ls_ord_prof.sort(key=chronology)
    global_stats = {'ord_profile' : ls_ord_prof,
    'scores' : all_sc,
    'score_ope' : (all_cong[0], all_cong[1]),
    'score_col' : (all_cong[2], all_cong[3]),
    'perf_ope' : float(all_cong[0])/all_cong[1],
    'perf_col' : float(all_cong[2])/all_cong[3]}
    return global_stats

def give_percent(scores) :
    nb_correct_ope, nb_ope, nb_correct_col, nb_col = scores
    correct_ope = nb_correct_ope / float(nb_ope)
    correct_col = nb_correct_col / float(nb_col)
    percents = ["Perf at operation level : {0:.0%}".format(correct_ope), "Perf at column level : {0:.0%}".format(correct_col)]
    return percents
