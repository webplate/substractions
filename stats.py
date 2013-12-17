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
import bugs

def all_scores(data, poss_sheets) :
    '''Precompute stats on whole dataset'''
    all_sc = {} #dominancy scores for all
    for subject in data :
        operations, poss_sheet = bugs.serialize(subject, poss_sheets)
        found_bugs = bugs.subject_sheet_bugs(subject['results'], operations)
        sc = bugs.dominancy(found_bugs, poss_sheet)
        if all_sc == {} :
            all_sc = sc
        for key in sc :
            all_sc[key] = (sc[key][0]+all_sc[key][0],
            sc[key][1]+all_sc[key][1])
    return all_sc

def all_congruency(data, poss_sheets) :
    nb_correct_ope = 0
    nb_correct_col = 0
    nb_ope = 0
    nb_col = 0
    for subject_id in range(len(data)) :#compute dominancies of subjects
        subject = data[subject_id]
        operations, poss_sheet = bugs.serialize(subject, poss_sheets)
        #create profile of subject (most dominant bugs)
        found_bugs = bugs.subject_sheet_bugs(subject['results'], operations)
        scores = bugs.dominancy(found_bugs, poss_sheet)
        dom_bugs = bugs.profile(scores, bugs.parameters.dominancy_thre,
        bugs.parameters.profile_size)
        #compute simulation according to profile
        b_simul_sheet = bugs.simulate(dom_bugs, poss_sheet)[1]
        scores = subject_congruency(subject_id, data, poss_sheet, b_simul_sheet,
        operations)
        nb_correct_ope += scores[0]
        nb_ope += scores[1]
        nb_correct_col += scores[2]
        nb_col += scores[3]
    return nb_correct_ope, nb_ope, nb_correct_col, nb_col

def subject_congruency(subject_id, data, poss_sheet, simul_sheet, operations) :
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

def give_percent(scores) :
    nb_correct_ope, nb_ope, nb_correct_col, nb_col = scores
    correct_ope = nb_correct_ope / float(nb_ope)
    correct_col = nb_correct_col / float(nb_col)
    percents = ["Perf at operation level : {0:.0%}".format(correct_ope), "Perf at column level : {0:.0%}".format(correct_col)]
    return percents
