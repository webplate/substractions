#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parameters to specify data of interest
dataPath = '../data/'
#~ subtractions = 'protocoleVanLehn'      #subtractions to resolve
subject_pattern = r's\d+\.\d+\.\d+'      #regex to find subject files
default_sub = 36    #default subject id in data
precomputation_path = 'precomputations/'

#Select subset of subject with condition
#subject[prop_test] == val_test AND subset == True
subset = True
prop_test = 'nb_ope'
val_test = 40

update_precomputation = False   #set to name of protocol once if change in protocol or in bug definitions
#possible values : False, 'protocoleVanLehn', 'protocoleAnalogue'
# Analysis settings
mental_limit = 10   #how much a student can substract in his mind (realistic attempt)
#~ dominancy_thre = 0.6    #threshold for picking dominant bugs
#~ profile_size = None
dominancy_thre = 0
profile_size = 4        #length of profile (nb of strategies)
tolerant = False     #be tolerant to +-1 errors from subjects
