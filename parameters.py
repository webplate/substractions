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
val_test = 20

if val_test == 40 :
    randomize = True
else :
    randomize = False

update_precomputation = False   #set to True once if change in protocol or in bug definitions
#possible values : 'protocoleVanLehn', 'protocoleAnalogue'
precomputations = 'protocoleVanLehn', 'protocoleAnalogue'
# Analysis settings
mental_limit = 20   #how much a student can substract in his mind (realistic attempt)
dom_thre = [0.2, 0.4, 0.6, 0.8]  #list of dominancy threshold for considering a bug used by subject
                                 #beware order is drawing order : start with lowest !

#~ dominancy_thre = 0.6    #threshold for picking dominant bugs in profile
#~ profile_size = None

#~ profile_size = [1,2,3,4,5,6]        #list of length of profile (nb of strategies)
profile_size = [3]
tolerant = False     #be tolerant to +-1 errors from subjects

blank = 'X'
#control bugId
check_exotic = True
zero_included = True
