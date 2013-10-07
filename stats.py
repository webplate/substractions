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

def all_scores(data, operations):
    '''Precompute stats on whole dataset'''
    all_sc = {} #dominancy scores for all
    poss_sheet = bugs.read_precomputations(bugs.parameters.precomputation_file)
    for subject in data :
        found_bugs = bugs.subject_sheet_bugs(subject['results'], operations)
        sc = bugs.dominancy(found_bugs, poss_sheet)
        if all_sc == {} :
            all_sc = sc
        for key in sc :
            all_sc[key] = (sc[key][0]+all_sc[key][0],
            sc[key][1]+all_sc[key][1])
    return all_sc
