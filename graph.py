#!/usr/bin/env python
# -*- coding: utf-8 -*-

#~ import numpy as np
import matplotlib.pyplot as plt
from graph_settings import *

def freq_by_type(scores) :
    N = len(scores)
    ind = range(N)
    #reorder scores for homogenous presentation
    freqs = [ [] for i in ind ]
    types = [ [] for i in ind ]
    i = 0
    for key in types_order :
        if key in scores :
            #compute frequencies of subject
            freqs[i] = float(scores[key][0]) / scores[key][1]
            types[i] = key
            i += 1
    return freqs, types, ind

def plot_scores(scores, all_scores):
    '''a bar plot showing frequency of appearance for each bug in scores
    '''
    freqs, types, ind = freq_by_type(scores)
    all_freqs = freq_by_type(all_scores)[0]
    #mean frequencies for all
    plt.bar(ind, all_freqs, facecolor='#333333')
    #grey barplot: frequencies of subject
    plt.bar(ind, freqs, facecolor='#777777', align='center')
    
    plt.xlabel('Bug types')
    plt.ylabel('Frequency of bugs')
    #no autoscale
    plt.ylim( (0, 1) )
    plt.title('Proportion of observed subject bugs')
    #rotated x axis labels
    plt.xticks(ind, types, rotation=90)
    #tuning to avoid cropped labels
    plt.subplots_adjust(bottom=0.35, top=0.95)


#~ sc = {'pt-gd=pt': (1, 26), "['blank', 'pt-gd=?']": (0, 11), 'N-0=0': (0, 4), "['blank', 'N-N=N']": (0, 1), "['blank', '0-N=N']": (0, 4), '0-N=N': (8, 9), "['blank', 'gd-pt']": (2, 11), "['blank', 'correct_col']": (0, 6), "['blank', '0-N=0']": (3, 4), 'gd-pt': (25, 26), "['blank', 'pt-gd=gd']": (0, 11), "['blank', 'pt-gd=0']": (3, 4), 'pt-gd=gd': (9, 26), 'pt-gd=?': (0, 26), 'pt-gd=0': (0, 26), '0-N=0': (0, 9), 'N-N=N': (0, 6), "['blank', 'pt-gd=pt']": (9, 11), 'incomplete': (5, 22)}
#~ plot_scores(sc, sc)
#~ plt.show()
