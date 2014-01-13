#!/usr/bin/env python
# -*- coding: utf-8 -*-

#~ import numpy as np
import matplotlib.pyplot as plt
from graph_settings import *
import bugs

def freq_by_type(scores) :
    N = len(scores)
    ind = range(N)
    #reorder scores for homogenous presentation
    freqs = [ 0 for i in ind ]
    types = [ '' for i in ind ]
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
    #~ print freqs
    #~ print ind
    #~ print all_scores, all_freqs
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

def plot_perf_duration(data):
    '''a bar plot showing performance by duration
    colors for judgement
    '''
    all_times = [subject['time'] for subject in data]
    all_perf = [subject['perf_col'] for subject in data]
    all_judge = []
    for subject in data :
        if 'judge' in subject :
            if subject['judge'] == 'A' :
                all_judge.append('green')
            elif subject['judge'] == 'B' :
                all_judge.append('orange')
            elif subject['judge'] == 'C' :
                all_judge.append('red')
        else:
            all_judge.append('white')
    
    plt.scatter(all_times, all_perf, c=all_judge, alpha=0.5, s=40)
    plt.xlabel('Duration of passation')
    plt.ylabel('Performance of simulation')
    #no autoscale
    plt.ylim( (0, 1) )
    plt.title('Performance over duration')

def  plot_len_plot(gstats_l) :
    '''plot perf for different profiles lenghts
    '''
    perfs = [stat['perf_col'] for stat in gstats_l]
    ind = range(1,len(perfs)+1)
    plt.bar(ind, perfs, facecolor='#333333', align='center')
    plt.xlabel('Longueur du profil de simulation')
    plt.ylabel('Performance de la simulation')
    #no autoscale
    plt.ylim( (0, 1) )
    plt.title('Effet de la longueur du profil cognitif')

def plot_prop_sub(gstats) :
    '''Proportion of subjects presenting bug
    for each bug'''
    
    bug_types = []
    bug_proportions = []
    for thresh in bugs.parameters.dom_thre :
        bug_counts = []
        repart = gstats['repartition'][thresh]
        for key in types_order :
            if key in repart :
                bug_counts.append(repart[key])
                if key not in bug_types :
                    bug_types.append(key)
        bug_proportions.append([float(count)/gstats['nb_subjects']
    for count in bug_counts])
    ind = range(len(bug_types))

    for i, thresh in enumerate(bugs.parameters.dom_thre) :
        plt.bar(ind, bug_proportions[i], align='center',
        facecolor=proportions_colors[i])
    
    plt.xlabel(u'Stratégies')
    plt.ylabel(u'Proportion de sujets') 
    plt.title(u'Répartition des bugs parmis les sujets')
    #no autoscale
    plt.ylim( (0, 1) )
    #rotated x axis labels
    plt.xticks(ind, bug_types, rotation=90)
    #tuning to avoid cropped labels
    plt.subplots_adjust(bottom=0.35, top=0.95)

#~ sc = {'pt-gd=pt': (1, 26), "['blank', 'pt-gd=?']": (0, 11), 'N-0=0': (0, 4), "['blank', 'N-N=N']": (0, 1), "['blank', '0-N=N']": (0, 4), '0-N=N': (8, 9), "['blank', 'gd-pt']": (2, 11), "['blank', 'correct_col']": (0, 6), "['blank', '0-N=0']": (3, 4), 'gd-pt': (25, 26), "['blank', 'pt-gd=gd']": (0, 11), "['blank', 'pt-gd=0']": (3, 4), 'pt-gd=gd': (9, 26), 'pt-gd=?': (0, 26), 'pt-gd=0': (0, 26), '0-N=0': (0, 9), 'N-N=N': (0, 6), "['blank', 'pt-gd=pt']": (9, 11), 'incomplete': (5, 22)}
#~ plot_scores(sc, sc)
#~ plt.show()
