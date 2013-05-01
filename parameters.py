#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parameters to specify data of interest
dataPath = '../data/'
subtractions = 'protocoleVanLehn'      #subtractions to resolve
reference = 'correctVanLehn'        #reference results
subject_pattern = r's\d+\.\d+\.\d+'      #regex to find subject files

# Analysis settings
mental_limit = 10   #how much a student can substract in his mind (realistic attempt)
