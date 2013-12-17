#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parameters to specify data of interest
dataPath = '../data/'
#~ subtractions = 'protocoleVanLehn'      #subtractions to resolve
subject_pattern = r's\d+\.\d+\.\d+'      #regex to find subject files
default_sub = 0    #default subject id in data
precomputation_path = 'precomputations/'

update_precomputation = False   #set to name of protocol once if change in protocol or in bug definitions

# Analysis settings
mental_limit = 10   #how much a student can substract in his mind (realistic attempt)
#~ dominancy_thre = 0.6    #threshold for picking dominant bugs
#~ profile_size = None
dominancy_thre = 0
profile_size = 7        #length of profile (nb of strategies)
tolerant = True     #be tolerant to +-1 errors from subjects
