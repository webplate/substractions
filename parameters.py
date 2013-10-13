#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parameters to specify data of interest
dataPath = '../data/'
subtractions = 'protocoleVanLehn'      #subtractions to resolve
reference = 'correctVanLehn'        #reference results
subject_pattern = r's\d+\.\d+\.\d+'      #regex to find subject files
default_sub = 0    #default subject id in data
precomputation_file = 'precomputed.pickle'

# Analysis settings
mental_limit = 10   #how much a student can substract in his mind (realistic attempt)
#~ dominancy_thre = 0.6    #threshold for picking dominant bugs
dominancy_thre = 0
profile_size = 4        #length of profile (nb of strategies)
tolerant = True     #be tolerant to +-1 errors from subjects
