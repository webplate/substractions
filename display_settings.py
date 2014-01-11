#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame.locals import *

#screen settings
full_screen = False
window_size = (800, 500)


#interface style
bg_color = (255, 255, 255)
txt_color = (0, 0, 0)
txt_font = "./fonts/UbuntuMono-R.ttf"
txt_size = 16
txt_inter = txt_size + 2
bug_color = (200, 200, 255)
correct_col_color = (200, 255, 200)
unexplained_color = (255, 200, 200)
incomplete_color = (0, 0, 255)

simul_txt_color = (55, 55, 55)
simul_good_color = (213, 255, 96)
simul_almost_color = (255, 195, 96)
simul_bad_color = (255, 103, 96)

note_font = "./fonts/UbuntuMono-R.ttf"
note_size = 12
note_inter = note_size

#subtractions pixel dimensions
sub_dims = (4* txt_size, 5* txt_inter)

#sheet params
sheet_dims = (8,5)
sheet_offset = (250,10)

#control settings
switch_key = K_s
strat_graph_key = K_g
sub_graph_key = K_h
proflen_graph_key = K_j

next_key = K_d
prev_key = K_q
next_button = 5
prev_button = 4
